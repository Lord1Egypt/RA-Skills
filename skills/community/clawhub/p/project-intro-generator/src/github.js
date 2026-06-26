const https = require('https');

function fetchGitHubRepoInfo(repoUrl) {
  return new Promise((resolve, reject) => {
    const match = repoUrl.match(/github\.com[/:]([\w-]+)\/([^\s/]+)/);
    if (!match) {
      return resolve(null);
    }
    const [owner, repo] = match.slice(1);
    const apiUrl = `https://api.github.com/repos/${owner}/${repo}`;

    const req = https.get(apiUrl, {
      headers: {
        'User-Agent': 'project-intro-generator',
        'Accept': 'application/vnd.github.v3+json'
      }
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.message && json.message.includes('Not Found')) {
            return resolve(null);
          }
          resolve({
            description: json.description || '',
            language: json.language || null,
            topics: json.topics || [],
            stargazers_count: json.stargazers_count || 0,
            forks_count: json.forks_count || 0,
            license: json.license ? json.license.name : null,
            html_url: json.html_url,
            created_at: json.created_at,
            updated_at: json.updated_at
          });
        } catch (e) {
          resolve(null);
        }
      });
    });

    req.on('error', () => { resolve(null); });
    req.setTimeout(5000, () => {
      req.destroy();
      resolve(null);
    });
  });
}

function inferProjectType(githubInfo, localStats) {
  if (!githubInfo) {
    return inferFromLocal(localStats);
  }

  const { description = '', language, topics = [] } = githubInfo;
  const text = `${description} ${topics.join(' ')}`.toLowerCase();

  const frontendIndicators = ['react', 'vue', 'angular', 'svelte', 'frontend', 'web', 'ui', 'frontend', 'website', 'app'];
  const backendIndicators = ['backend', 'api', 'server', 'backend', 'express', 'koa', 'nest', 'fastify', 'rest', 'graphql'];

  const frontendScore = frontendIndicators.filter(w => text.includes(w)).length;
  const backendScore = backendIndicators.filter(w => text.includes(w)).length;

  if (language) {
    const jsLangs = ['JavaScript', 'TypeScript'];
    const frontendLangs = ['JavaScript', 'TypeScript', 'HTML', 'CSS'];
    const backendLangs = ['JavaScript', 'TypeScript', 'Python', 'Go', 'Java', 'Ruby', 'Rust', 'PHP'];

    if (frontendLangs.includes(language) && frontendScore > backendScore) {
      return { kind: 'frontend', language, source: 'github' };
    }
    if (backendLangs.includes(language) && backendScore > frontendScore) {
      return { kind: 'backend', language, source: 'github' };
    }
  }

  if (frontendScore > backendScore && frontendScore > 0) {
    return { kind: 'frontend', language: language || null, source: 'github' };
  }
  if (backendScore > frontendScore && backendScore > 0) {
    return { kind: 'backend', language: language || null, source: 'github' };
  }

  return { kind: 'unknown', language: language || null, source: 'github' };
}

function inferFromLocal(stats) {
  const { languages = [], controllers = [], services = [], routes = [], components = [], pages = [], htmlFiles = [] } = stats;

  const hasBackend = controllers.length > 0 || services.length > 0 || routes.length > 0;
  const hasFrontend = components.length > 0 || pages.length > 0 || htmlFiles.length > 0;

  const mainLang = languages.length > 0 ? languages[0].name : null;

  if (hasFrontend && hasBackend) {
    return { kind: 'fullstack', language: mainLang, source: 'local' };
  }
  if (hasBackend) {
    return { kind: 'backend', language: mainLang, source: 'local' };
  }
  if (hasFrontend) {
    return { kind: 'frontend', language: mainLang, source: 'local' };
  }

  return { kind: 'unknown', language: mainLang, source: 'local' };
}

module.exports = {
  fetchGitHubRepoInfo,
  inferProjectType
};
