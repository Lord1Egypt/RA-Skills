import { getClient } from '../client.js';

export async function listRepos(options: { org?: string }) {
  const client = getClient();

  try {
    let repos;
    if (options.org) {
      // Use direct API call for org repos
      repos = await client.client.get(`/orgs/${options.org}/repos`);
    } else {
      // List repos for authenticated user
      repos = await client.repos.listForAuthenticatedUser();
    }
    console.log(JSON.stringify(repos, null, 2));
  } catch (error) {
    console.error('Error listing repos:', error);
    process.exit(1);
  }
}

export async function getRepoInfo(options: { owner: string; repo: string }) {
  const client = getClient();

  try {
    const repo = await client.repos.get(options.owner, options.repo);
    console.log(JSON.stringify(repo, null, 2));
  } catch (error) {
    console.error('Error getting repo info:', error);
    process.exit(1);
  }
}
