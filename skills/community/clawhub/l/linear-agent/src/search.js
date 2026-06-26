/**
 * src/search.js
 * Full-text issue search using Linear's search API.
 *
 * Linear exposes a dedicated `searchIssues` query that performs
 * relevance-ranked full-text search across title and description.
 */

'use strict';

const SEARCH_ISSUE_FRAGMENT = `
  id
  identifier
  title
  description
  priority
  priorityLabel
  url
  createdAt
  updatedAt
  state {
    id
    name
    type
    color
  }
  assignee {
    id
    name
    email
  }
  team {
    id
    name
    key
  }
  labels {
    nodes {
      id
      name
      color
    }
  }
  cycle {
    id
    name
    number
  }
  project {
    id
    name
  }
`;

// ---------------------------------------------------------------------------
// searchIssues
// ---------------------------------------------------------------------------

/**
 * Full-text search across issues.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string}  params.query  - Search query string
 * @param {string} [params.teamId]- Narrow results to a specific team
 * @param {number} [params.first] - Max results (default 25)
 * @returns {Promise<object>}
 */
async function searchIssues(client, params) {
  const { query, teamId, first = 25 } = params;

  if (!query || !query.trim()) {
    throw new Error('"query" is required and must not be empty.');
  }

  // Linear has a dedicated searchIssues query for relevance-ranked results
  const gql = `
    query SearchIssues($query: String!, $filter: IssueFilter, $first: Int) {
      searchIssues(query: $query, filter: $filter, first: $first) {
        nodes {
          ${SEARCH_ISSUE_FRAGMENT}
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  `;

  const filter = {};
  if (teamId) filter.team = { id: { eq: teamId } };

  const data = await client.request(gql, {
    query: query.trim(),
    filter: Object.keys(filter).length ? filter : undefined,
    first: Number(first),
  });

  const results = data.searchIssues.nodes;

  return {
    success: true,
    query: query.trim(),
    data: results,
    count: results.length,
    pageInfo: data.searchIssues.pageInfo,
  };
}

module.exports = { searchIssues };
