/**
 * src/comments.js
 * Post and manage comments on Linear issues.
 */

'use strict';

const { resolveIssueId } = require('./issues');

// ---------------------------------------------------------------------------
// postComment
// ---------------------------------------------------------------------------

/**
 * Post a comment on a Linear issue.
 * Accepts either a UUID or an identifier (e.g. "ENG-123") for the issue.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string} params.issueId - Issue UUID or identifier
 * @param {string} params.body    - Comment body (supports markdown)
 * @returns {Promise<object>}
 */
async function postComment(client, params) {
  const { issueId, body } = params;

  if (!issueId) throw new Error('"issueId" is required to post a comment.');
  if (!body)    throw new Error('"body" is required to post a comment.');

  // Resolve identifier → UUID if necessary
  const resolvedIssueId = await resolveIssueId(client, issueId);

  const mutation = `
    mutation CreateComment($input: CommentCreateInput!) {
      commentCreate(input: $input) {
        success
        comment {
          id
          body
          createdAt
          updatedAt
          url
          user {
            id
            name
            email
          }
          issue {
            id
            identifier
            title
          }
        }
      }
    }
  `;

  const data = await client.request(mutation, {
    input: { issueId: resolvedIssueId, body },
  });

  if (!data.commentCreate.success) {
    throw new Error('Linear returned success=false for commentCreate.');
  }

  return {
    success: true,
    data: data.commentCreate.comment,
  };
}

module.exports = { postComment };
