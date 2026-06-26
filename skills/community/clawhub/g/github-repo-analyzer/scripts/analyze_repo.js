#!/usr/bin/env node
/**
 * GitHub Repo Analyzer
 */

const https = require('https');

function fetchGitHub(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.github.com',
      path: path,
      method: 'GET',
      headers: {
        'User-Agent': 'OpenClaw-Skill',
        'Accept': 'application/vnd.github.v3+json'
      }
    };

    https.get(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function analyzeRepo(owner, repo) {
  try {
    const repoData = await fetchGitHub(`/repos/${owner}/${repo}`);
    const languages = await fetchGitHub(`/repos/${owner}/${repo}/languages`);
    const contributors = await fetchGitHub(`/repos/${owner}/${repo}/contributors?per_page=10`);

    const result = {
      name: repoData.full_name,
      description: repoData.description,
      stats: {
        stars: repoData.stargazers_count,
        forks: repoData.forks_count,
        watchers: repoData.watchers_count,
        openIssues: repoData.open_issues_count,
        size: repoData.size
      },
      languages: languages,
      topContributors: contributors.slice(0, 5).map(c => ({
        login: c.login,
        contributions: c.contributions
      })),
      dates: {
        created: repoData.created_at,
        updated: repoData.updated_at,
        pushed: repoData.pushed_at
      },
      license: repoData.license ? repoData.license.name : 'None',
      homepage: repoData.homepage,
      topics: repoData.topics || []
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

const repoUrl = process.argv[2];
if (!repoUrl) {
  console.error('Usage: node analyze_repo.js owner/repo');
  process.exit(1);
}

const match = repoUrl.match(/github\.com\/([^\/]+)\/([^\/]+)/);
if (match) {
  analyzeRepo(match[1], match[2]);
} else {
  const parts = repoUrl.split('/');
  if (parts.length === 2) {
    analyzeRepo(parts[0], parts[1]);
  } else {
    console.error('Invalid repo format. Use: owner/repo or github.com/owner/repo');
    process.exit(1);
  }
}
