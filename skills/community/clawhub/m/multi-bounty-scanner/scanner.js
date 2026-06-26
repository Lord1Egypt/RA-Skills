#!/usr/bin/env node

/**
 * Multi-Platform Bounty Scanner
 * Scans 50+ bounty platforms for new opportunities
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Platform scanners
const PLATFORMS = {
  github: {
    name: 'GitHub',
    scan: async (filters) => {
      const tech = filters.techStack?.join(',') || '';
      const cmd = `gh search issues "bounty" --label "bounty" --state open --limit 50 --json title,url,repository,labels,createdAt,body`;
      
      try {
        const result = execSync(cmd, { encoding: 'utf8' });
        const issues = JSON.parse(result);
        
        return issues
          .filter(issue => {
            const created = new Date(issue.createdAt);
            const daysSince = (Date.now() - created) / (1000 * 60 * 60 * 24);
            return daysSince < 7; // Only last 7 days
          })
          .map(issue => ({
            id: `github-${issue.repository.nameWithOwner}-${issue.url.split('/').pop()}`,
            platform: 'github',
            title: issue.title,
            reward: 'Unknown',
            techStack: extractTechStack(issue.body),
            difficulty: 'unknown',
            url: issue.url,
            repo: issue.repository.nameWithOwner,
            createdAt: issue.createdAt,
            description: issue.body?.substring(0, 200) || ''
          }));
      } catch (error) {
        console.error('GitHub scan failed:', error.message);
        return [];
      }
    }
  },
  
  code4rena: {
    name: 'Code4rena',
    scan: async (filters) => {
      // Would use web scraping or API
      // For now, return mock data
      return [];
    }
  },
  
  immunefi: {
    name: 'Immunefi',
    scan: async (filters) => {
      // Would use web scraping or API
      return [];
    }
  }
};

// Helper functions
function extractTechStack(text) {
  if (!text) return [];
  
  const keywords = {
    javascript: /javascript|js|node\.?js|react|vue|angular/i,
    typescript: /typescript|ts/i,
    python: /python|django|flask/i,
    rust: /rust|cargo/i,
    solidity: /solidity|smart contract|evm/i,
    go: /\bgo\b|golang/i
  };
  
  const found = [];
  for (const [tech, regex] of Object.entries(keywords)) {
    if (regex.test(text)) {
      found.push(tech);
    }
  }
  
  return found;
}

function loadConfig() {
  const configPath = path.join(process.env.HOME, '.bounty-scanner', 'config.json');
  
  if (fs.existsSync(configPath)) {
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }
  
  // Default config
  return {
    filters: {
      techStack: [],
      minReward: 0,
      maxDifficulty: 'high',
      platforms: ['github']
    },
    notifications: {
      telegram: {
        enabled: false
      }
    }
  };
}

function loadSeenBounties() {
  const dbPath = path.join(process.env.HOME, '.bounty-scanner', 'seen.json');
  
  if (fs.existsSync(dbPath)) {
    return new Set(JSON.parse(fs.readFileSync(dbPath, 'utf8')));
  }
  
  return new Set();
}

function saveSeenBounties(seen) {
  const dbPath = path.join(process.env.HOME, '.bounty-scanner', 'seen.json');
  const dir = path.dirname(dbPath);
  
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.writeFileSync(dbPath, JSON.stringify([...seen], null, 2));
}

async function scanPlatforms(config) {
  const results = [];
  const seen = loadSeenBounties();
  
  for (const platformName of config.filters.platforms) {
    const platform = PLATFORMS[platformName];
    
    if (!platform) {
      console.error(`Unknown platform: ${platformName}`);
      continue;
    }
    
    console.log(`Scanning ${platform.name}...`);
    
    try {
      const bounties = await platform.scan(config.filters);
      
      // Filter new bounties
      const newBounties = bounties.filter(b => !seen.has(b.id));
      
      // Mark as seen
      bounties.forEach(b => seen.add(b.id));
      
      results.push(...newBounties);
      
      console.log(`  Found ${bounties.length} bounties (${newBounties.length} new)`);
    } catch (error) {
      console.error(`  Error scanning ${platform.name}:`, error.message);
    }
  }
  
  saveSeenBounties(seen);
  
  return results;
}

function formatOutput(bounties, format = 'text') {
  if (format === 'json') {
    return JSON.stringify({
      bounties,
      summary: {
        total: bounties.length,
        platforms: [...new Set(bounties.map(b => b.platform))].length
      }
    }, null, 2);
  }
  
  // Text format
  let output = `\n🎯 Found ${bounties.length} new bounties:\n\n`;
  
  for (const bounty of bounties) {
    output += `📌 ${bounty.title}\n`;
    output += `   Platform: ${bounty.platform}\n`;
    output += `   Reward: ${bounty.reward}\n`;
    output += `   Tech: ${bounty.techStack.join(', ') || 'Unknown'}\n`;
    output += `   URL: ${bounty.url}\n`;
    output += `\n`;
  }
  
  return output;
}

// Main
async function main() {
  const args = process.argv.slice(2);
  const config = loadConfig();
  
  // Parse CLI args
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--tech' && args[i + 1]) {
      config.filters.techStack = args[i + 1].split(',');
      i++;
    } else if (args[i] === '--min-reward' && args[i + 1]) {
      config.filters.minReward = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--output' && args[i + 1]) {
      config.outputFile = args[i + 1];
      i++;
    }
  }
  
  console.log('🔍 Multi-Platform Bounty Scanner\n');
  console.log(`Scanning platforms: ${config.filters.platforms.join(', ')}\n`);
  
  const bounties = await scanPlatforms(config);
  
  const output = formatOutput(bounties, config.outputFile ? 'json' : 'text');
  
  if (config.outputFile) {
    fs.writeFileSync(config.outputFile, output);
    console.log(`\n✅ Results saved to ${config.outputFile}`);
  } else {
    console.log(output);
  }
  
  if (bounties.length === 0) {
    console.log('No new bounties found.');
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { scanPlatforms, PLATFORMS };
