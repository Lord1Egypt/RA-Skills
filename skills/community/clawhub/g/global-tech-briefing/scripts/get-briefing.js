#!/usr/bin/env node

const { exec } = require('child_process');
const date = process.argv[2] || new Date().toISOString().split('T')[0];

// Run web searches for tech trends, company news, and AI/quantum
const searchQueries = [
  'top global tech trends today',
  'major tech company announcements today',
  'AI quantum computing latest news'
];

exec('node -e "const web = require(\'@openclaw/web\'); webSearch({ query: \'' + searchQueries[0] + '\', count: 2 })", (err, stdout1) => {
  exec('node -e "const web = require(\'@openclaw/web\'); webSearch({ query: \'' + searchQueries[1] + '\', count: 2 })", (err2, stdout2) => {
    exec('node -e "const web = require(\'@openclaw/web\'); webSearch({ query: \'' + searchQueries[2] + '\', count: 1 })", (err3, stdout3) => {
      // Parse search results for key takeaways
      const trends = stdout1.split('\n').slice(0, 2);
      const companies = stdout2.split('\n').slice(0, 2);
      const aiq = stdout3.split('\n').slice(0, 1);

      // Structure the briefing
      const briefing = `
[Global Tech Briefing: ${date}]
Key Trends:
  - ${trends[0] || 'No major trends found'}
  - ${trends[1] || 'No additional trends'}
  - ${aiq[0] || 'No major AI/quantum news'}
Company News:
  - ${companies[0] || 'No major company announcements'}
  - ${companies[1] || 'No additional company news'}
Key Takeaways:
  - Keep an eye on AI and quantum advancements
  - Monitor large tech company moves and funding
`;

      // Remove extra whitespace
      const cleanBriefing = briefing.trim().replace(/\n\s+/g, '\n');
      console.log(cleanBriefing);
    });
  });
});
