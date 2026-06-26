#!/usr/bin/env node
/**
 * OpenRouter Rankings Fetcher (Full Version)
 * 
 * Usage: node fetch.js [--save] [--json]
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(process.env.HOME, '.openclaw', 'data', 'openrouter-rankings');
const URL = 'https://openrouter.ai/rankings';

const args = process.argv.slice(2);
const shouldSave = args.includes('--save');
const shouldJson = args.includes('--json');

// Known provider names
const KNOWN_PROVIDERS = [
  'google', 'anthropic', 'openai', 'minimax', 'deepseek', 'stepfun', 
  'x-ai', 'qwen', 'moonshotai', 'arcee-ai', 'zhipu', 'meta-llama',
  'mistralai', 'cohere', 'stability-ai', 'amazon', 'microsoft'
];

async function extractData(page) {
  return await page.evaluate((knownProviders) => {
    const result = {
      fetchedAt: new Date().toISOString(),
      source: window.location.href,
      period: 'This Week',
      topModels: [],
      marketShare: [],
      topApps: [],
      highlights: {}
    };

    // 1. Extract Top Models
    const allLinks = document.querySelectorAll('a[href^="/"]');
    const modelData = [];
    
    allLinks.forEach(link => {
      const href = link.getAttribute('href');
      const parts = href.split('/').filter(p => p);
      
      // Check if it's a model link: /provider/model-name
      if (parts.length === 2 && knownProviders.includes(parts[0])) {
        const provider = parts[0];
        const model = link.textContent.trim();
        
        // Skip navigation links
        if (model.length < 3 || model.toLowerCase().includes('docs')) return;
        
        // Find the parent container with tokens info
        let container = link.closest('div');
        let searchDepth = 0;
        let tokens = '';
        let change = '';
        
        // Search up to 5 levels for tokens
        while (container && searchDepth < 5) {
          const text = container.innerText || '';
          const tokensMatch = text.match(/(\d+\.?\d*[TB])\s*tokens?/i);
          
          if (tokensMatch) {
            tokens = tokensMatch[1];
            // Find change percentage
            const changeMatch = text.match(/(-?\d+)%/);
            if (changeMatch && !text.includes(tokensMatch[0] + changeMatch[0])) {
              change = changeMatch[1] + '%';
            }
            break;
          }
          
          container = container.parentElement;
          searchDepth++;
        }
        
        if (tokens) {
          modelData.push({ model, provider, tokens, change });
        }
      }
    });
    
    // Deduplicate and limit to 20
    const seenModels = new Set();
    modelData.forEach(m => {
      if (!seenModels.has(m.model) && result.topModels.length < 20) {
        seenModels.add(m.model);
        result.topModels.push({
          rank: result.topModels.length + 1,
          ...m
        });
      }
    });

    // 2. Extract Market Share from buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
      const text = btn.textContent.trim();
      const lines = text.split('\n').map(l => l.trim()).filter(l => l);
      
      // Match: "1.\nprovider\nXXXB\nXX.X%"
      if (lines.length >= 4 && lines[0].match(/^\d+\.$/)) {
        const rank = parseInt(lines[0]);
        const provider = lines[1];
        const tokens = lines[2];
        const share = lines[3];
        
        if (tokens && tokens.match(/\d+[TB]/i) && share && share.match(/\d+\.\d+%/)) {
          result.marketShare.push({ rank, provider, tokens, share });
        }
      }
    });
    result.marketShare = result.marketShare.slice(0, 10);

    // 3. Extract Top Apps
    const appLinks = document.querySelectorAll('a[href*="/apps?url="]');
    const seenApps = new Set();
    
    appLinks.forEach(link => {
      const appName = link.textContent.trim();
      if (seenApps.has(appName) || appName.length < 2) return;
      
      // Find parent with tokens
      let container = link.closest('div');
      let searchDepth = 0;
      let tokens = '';
      let description = '';
      
      while (container && searchDepth < 5) {
        const text = container.innerText || '';
        const tokensMatch = text.match(/(\d+\.?\d*[TB])\s*tokens?/i);
        
        if (tokensMatch) {
          tokens = tokensMatch[1];
          // Extract description (line after app name)
          const lines = text.split('\n').map(l => l.trim());
          for (let i = 0; i < lines.length; i++) {
            if (lines[i] === appName && lines[i + 1] && !lines[i + 1].match(/\d+[TB]/i)) {
              description = lines[i + 1];
              break;
            }
          }
          break;
        }
        
        container = container.parentElement;
        searchDepth++;
      }
      
      if (tokens && !seenApps.has(appName)) {
        seenApps.add(appName);
        result.topApps.push({
          rank: result.topApps.length + 1,
          app: appName,
          description,
          tokens
        });
      }
    });
    result.topApps = result.topApps.slice(0, 10);

    // 4. Highlights
    const fastestGrowing = result.topModels
      .filter(m => m.change && parseInt(m.change) > 20)
      .sort((a, b) => parseInt(b.change) - parseInt(a.change))[0];
    
    if (fastestGrowing) {
      result.highlights.fastestGrowing = `${fastestGrowing.model} (${fastestGrowing.change})`;
    }
    if (result.topModels[0]) {
      result.highlights.topModel = `${result.topModels[0].model} (${result.topModels[0].tokens})`;
    }
    if (result.topApps[0]) {
      result.highlights.topApp = `${result.topApps[0].app} (${result.topApps[0].tokens})`;
    }
    if (result.marketShare[0]) {
      result.highlights.topProvider = `${result.marketShare[0].provider} (${result.marketShare[0].share})`;
    }

    return result;
  }, KNOWN_PROVIDERS);
}

function formatReport(data) {
  let report = `# OpenRouter Rankings Report\n\n`;
  report += `📅 **Date**: ${new Date(data.fetchedAt).toLocaleDateString('zh-CN')} (This Week)\n\n`;
  report += `---\n\n`;
  
  // Top Models
  report += `## 🏆 Top Models (${data.topModels.length} total)\n\n`;
  report += `| Rank | Model | Provider | Tokens | Change |\n`;
  report += `|------|-------|----------|--------|--------|\n`;
  data.topModels.forEach(m => {
    report += `| ${m.rank} | ${m.model} | ${m.provider || '-'} | ${m.tokens} | ${m.change || '-'} |\n`;
  });
  
  // Market Share
  if (data.marketShare.length > 0) {
    report += `\n---\n\n`;
    report += `## 📊 Market Share\n\n`;
    report += `| Rank | Provider | Tokens | Share |\n`;
    report += `|------|----------|--------|-------|\n`;
    data.marketShare.forEach(p => {
      report += `| ${p.rank} | ${p.provider} | ${p.tokens} | ${p.share} |\n`;
    });
  }
  
  // Top Apps
  report += `\n---\n\n`;
  report += `## 📱 Top Apps (${data.topApps.length} total)\n\n`;
  report += `| Rank | App | Description | Tokens |\n`;
  report += `|------|-----|-------------|--------|\n`;
  data.topApps.forEach(a => {
    report += `| ${a.rank} | **${a.app}** | ${a.description || '-'} | ${a.tokens} |\n`;
  });
  
  // Highlights
  report += `\n---\n\n`;
  report += `## 🚀 Highlights\n\n`;
  if (data.highlights.topModel) report += `- **#1 Model**: ${data.highlights.topModel}\n`;
  if (data.highlights.fastestGrowing) report += `- **Fastest Growing**: ${data.highlights.fastestGrowing}\n`;
  if (data.highlights.topApp) report += `- **#1 App**: ${data.highlights.topApp}\n`;
  if (data.highlights.topProvider) report += `- **#1 Provider**: ${data.highlights.topProvider}\n`;
  
  return report;
}

(async () => {
  console.log('🚀 Fetching OpenRouter Rankings...');
  const startTime = Date.now();
  
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.CHROMIUM_PATH || 
      '/home/Admin/.cache/ms-playwright/chromium-1194/chrome-linux/chrome'
  });
  
  const page = await browser.newPage();
  
  console.log(`📱 Navigating to: ${URL}`);
  await page.goto(URL, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  
  // Click "Show more" for Top Models
  try {
    const showMoreBtn = await page.$('button:has-text("Show more")');
    if (showMoreBtn) {
      console.log('📄 Loading more models...');
      await showMoreBtn.click();
      await page.waitForTimeout(2000);
    }
  } catch (e) {}
  
  // Scroll to load Market Share section
  try {
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight / 2);
    });
    await page.waitForTimeout(1000);
  } catch (e) {}
  
  const data = await extractData(page);
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
  
  console.log(`\n✅ Fetched in ${elapsed}s\n`);
  
  // Print report
  const report = formatReport(data);
  console.log(report);
  
  // Save
  if (shouldSave) {
    const today = new Date().toISOString().split('T')[0];
    const jsonPath = path.join(DATA_DIR, `${today}.json`);
    const mdPath = path.join(DATA_DIR, `${today}.md`);
    
    if (!fs.existsSync(DATA_DIR)) {
      fs.mkdirSync(DATA_DIR, { recursive: true });
    }
    
    fs.writeFileSync(jsonPath, JSON.stringify(data, null, 2));
    fs.writeFileSync(mdPath, report);
    console.log(`\n💾 Saved:\n   - ${jsonPath}\n   - ${mdPath}`);
  }
  
  // JSON output
  if (shouldJson) {
    console.log('\n```json');
    console.log(JSON.stringify(data, null, 2));
    console.log('```');
  }
  
  await browser.close();
})();
