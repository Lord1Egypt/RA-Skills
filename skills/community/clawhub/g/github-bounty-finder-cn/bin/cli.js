#!/usr/bin/env node

/**
 * GitHub Bounty Finder CLI
 * Scan for high-value GitHub and Algora bounties
 */

const { Command } = require('commander');
const chalk = require('chalk');
const BountyScanner = require('../src/scanner');
require('dotenv').config();

const program = new Command();

program
  .name('github-bounty-finder')
  .description('Find high-value GitHub and Algora bounties with low competition')
  .version('1.0.0');

program
  .command('scan')
  .description('Scan for bounties')
  .option('-q, --query <query>', 'Search query', 'bounty')
  .option('-l, --limit <number>', 'Max results', '50')
  .option('-m, --min-bounty <amount>', 'Minimum bounty amount (USD)', '100')
  .option('-c, --max-competition <number>', 'Max competition (comments)', '5')
  .option('--github-only', 'Scan GitHub only')
  .option('--algora-only', 'Scan Algora only')
  .option('-o, --output <file>', 'Output to JSON file')
  .action(async (options) => {
    console.log(chalk.bold.blue('\n🎯 GitHub Bounty Finder v1.0.0\n'));
    
    // Validate API tokens
    if (!process.env.GITHUB_TOKEN && !options.algoraOnly) {
      console.warn(chalk.yellow('⚠️  Warning: GITHUB_TOKEN not set. GitHub scanning disabled.'));
    }
    if (!process.env.ALGORA_API_KEY && !options.githubOnly) {
      console.warn(chalk.yellow('⚠️  Warning: ALGORA_API_KEY not set. Algora scanning disabled.'));
    }

    const scanner = new BountyScanner();
    
    const results = await scanner.scan({
      github: !options.algoraOnly,
      algora: !options.githubOnly,
      query: options.query,
      limit: parseInt(options.limit),
      minBounty: parseInt(options.minBounty),
      maxCompetition: parseInt(options.maxCompetition)
    });

    // Display results
    console.log(chalk.bold.green(`\n📊 Scan Results:\n`));
    console.log(`   Total Bounties Found: ${chalk.bold(results.totalFound)}`);
    console.log(`   🔥 High Priority: ${chalk.red(results.highPriority)}`);
    console.log(`   ✅ Good Opportunities: ${chalk.green(results.goodOpportunities)}`);
    console.log(`   Scanned At: ${results.scannedAt}\n`);

    if (results.bounties.length > 0) {
      console.log(chalk.bold.blue('\n🏆 Top Opportunities:\n'));
      
      results.bounties.slice(0, 10).forEach((bounty, index) => {
        const emoji = bounty.score >= 80 ? '🔥' : bounty.score >= 60 ? '✅' : '⚠️';
        console.log(`${emoji} #${index + 1} [Score: ${bounty.score}/100]`);
        console.log(`   Title: ${bounty.title}`);
        console.log(`   URL: ${chalk.cyan(bounty.url)}`);
        if (bounty.bountyAmount) {
          console.log(`   Bounty: ${chalk.green(`$${bounty.bountyAmount}`)}`);
        }
        console.log(`   Competition: ${bounty.competitionLevel} (${bounty.comments || 0} comments)`);
        console.log(`   ${bounty.recommendedAction}\n`);
      });

      // Pricing recommendation
      console.log(chalk.bold.yellow('\n💰 Pricing Recommendation:\n'));
      console.log(`   Recommended Price: ${chalk.green(`$${results.pricingRecommendation.recommendedPrice}/month`)}`);
      console.log(`   Justification: ${results.pricingRecommendation.justification}\n`);
    } else {
      console.log(chalk.yellow('\n⚠️  No bounties found matching your criteria.\n'));
    }

    // Save to file if requested
    if (options.output) {
      const fs = require('fs');
      fs.writeFileSync(options.output, JSON.stringify(results, null, 2));
      console.log(chalk.green(`\n💾 Results saved to: ${options.output}\n`));
    }
  });

program
  .command('config')
  .description('Show configuration status')
  .action(() => {
    console.log(chalk.bold.blue('\n⚙️  Configuration Status:\n'));
    console.log(`   GITHUB_TOKEN: ${process.env.GITHUB_TOKEN ? chalk.green('✓ Set') : chalk.red('✗ Not set')}`);
    console.log(`   ALGORA_API_KEY: ${process.env.ALGORA_API_KEY ? chalk.green('✓ Set') : chalk.red('✗ Not set')}\n`);
    
    if (!process.env.GITHUB_TOKEN || !process.env.ALGORA_API_KEY) {
      console.log(chalk.yellow('📝 Create a .env file with:\n'));
      console.log('   GITHUB_TOKEN=your_github_token');
      console.log('   ALGORA_API_KEY=your_algora_api_key\n');
    }
  });

program
  .command('demo')
  .description('Run demo scan with sample data')
  .action(async () => {
    console.log(chalk.bold.blue('\n🎯 GitHub Bounty Finder - Demo Mode\n'));
    
    const sampleBounties = [
      {
        id: 1,
        title: 'Fix memory leak in data processing module',
        url: 'https://github.com/example/repo/issues/123',
        bountyAmount: 1500,
        comments: 0,
        createdAt: new Date().toISOString(),
        score: 95,
        competitionLevel: 'None',
        recommendedAction: '🔥 HIGH PRIORITY - Apply immediately'
      },
      {
        id: 2,
        title: 'Implement OAuth2 authentication',
        url: 'https://github.com/example/repo/issues/456',
        bountyAmount: 800,
        comments: 2,
        createdAt: new Date(Date.now() - 86400000 * 2).toISOString(),
        score: 78,
        competitionLevel: 'Low',
        recommendedAction: '✅ GOOD OPPORTUNITY - Consider applying'
      },
      {
        id: 3,
        title: 'Add TypeScript support',
        url: 'https://github.com/example/repo/issues/789',
        bountyAmount: 500,
        comments: 1,
        createdAt: new Date(Date.now() - 86400000 * 5).toISOString(),
        score: 72,
        competitionLevel: 'Low',
        recommendedAction: '✅ GOOD OPPORTUNITY - Consider applying'
      }
    ];

    console.log(chalk.bold.green('\n📊 Sample Results:\n'));
    console.log(`   Total Bounties: ${chalk.bold(3)}`);
    console.log(`   🔥 High Priority: ${chalk.red(1)}`);
    console.log(`   ✅ Good Opportunities: ${chalk.green(2)}\n`);

    console.log(chalk.bold.blue('\n🏆 Top Opportunities:\n'));
    sampleBounties.forEach((bounty, index) => {
      const emoji = bounty.score >= 80 ? '🔥' : '✅';
      console.log(`${emoji} #${index + 1} [Score: ${bounty.score}/100]`);
      console.log(`   Title: ${bounty.title}`);
      console.log(`   URL: ${chalk.cyan(bounty.url)}`);
      console.log(`   Bounty: ${chalk.green(`$${bounty.bountyAmount}`)}`);
      console.log(`   Competition: ${bounty.competitionLevel} (${bounty.comments} comments)`);
      console.log(`   ${bounty.recommendedAction}\n`);
    });

    console.log(chalk.bold.yellow('\n💰 This tool can help you find $3,000-8,000/month in bounties!\n'));
  });

// Parse arguments
program.parse(process.argv);

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
