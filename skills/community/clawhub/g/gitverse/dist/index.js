import { Command } from 'commander';
import 'dotenv/config';
import * as repos from './commands/repos.js';
import * as issues from './commands/issues.js';
import * as pulls from './commands/pulls.js';
const program = new Command();
program
    .name('gitverse')
    .description('GitVerse CLI for OpenClaw')
    .version('1.0.0');
// Repos commands
const reposCmd = program.command('repos').description('Repository commands');
reposCmd
    .command('list')
    .description('List repositories for authenticated user or organization')
    .option('--org <org>', 'Organization name')
    .action(repos.listRepos);
reposCmd
    .command('info')
    .description('Get repository info')
    .requiredOption('--owner <owner>', 'Repository owner')
    .requiredOption('--repo <repo>', 'Repository name')
    .action(repos.getRepoInfo);
// Issues commands
const issuesCmd = program.command('issues').description('Issue commands');
issuesCmd
    .command('list')
    .description('List issues')
    .requiredOption('--owner <owner>', 'Repository owner')
    .requiredOption('--repo <repo>', 'Repository name')
    .option('--state <state>', 'Issue state (open, closed, all)', 'all')
    .action(issues.listIssues);
issuesCmd
    .command('view')
    .description('View issue')
    .requiredOption('--owner <owner>', 'Repository owner')
    .requiredOption('--repo <repo>', 'Repository name')
    .requiredOption('--number <number>', 'Issue number', parseInt)
    .action(issues.getIssue);
issuesCmd
    .command('comments')
    .description('List issue comments')
    .requiredOption('--owner <owner>', 'Repository owner')
    .requiredOption('--repo <repo>', 'Repository name')
    .requiredOption('--number <number>', 'Issue number', parseInt)
    .action(issues.listComments);
// Pulls commands
const pullsCmd = program.command('pulls').description('Pull request commands');
pullsCmd
    .command('list')
    .description('List pull requests')
    .requiredOption('--owner <owner>', 'Repository owner')
    .requiredOption('--repo <repo>', 'Repository name')
    .option('--state <state>', 'PR state (open, closed, all)', 'all')
    .action(pulls.listPulls);
pullsCmd
    .command('view')
    .description('View pull request')
    .requiredOption('--owner <owner>', 'Repository owner')
    .requiredOption('--repo <repo>', 'Repository name')
    .requiredOption('--number <number>', 'PR number', parseInt)
    .action(pulls.getPull);
pullsCmd
    .command('create')
    .description('Create pull request')
    .requiredOption('--owner <owner>', 'Repository owner')
    .requiredOption('--repo <repo>', 'Repository name')
    .requiredOption('--title <title>', 'PR title')
    .requiredOption('--head <head>', 'Head branch')
    .requiredOption('--base <base>', 'Base branch')
    .option('--body <body>', 'PR body')
    .action(pulls.createPull);
pullsCmd
    .command('commits')
    .description('List pull request commits')
    .requiredOption('--owner <owner>', 'Repository owner')
    .requiredOption('--repo <repo>', 'Repository name')
    .requiredOption('--number <number>', 'PR number', parseInt)
    .action(pulls.listPullCommits);
pullsCmd
    .command('files')
    .description('List pull request files')
    .requiredOption('--owner <owner>', 'Repository owner')
    .requiredOption('--repo <repo>', 'Repository name')
    .requiredOption('--number <number>', 'PR number', parseInt)
    .action(pulls.listPullFiles);
program.parse();
