import { getClient } from '../client.js';
export async function listPulls(options) {
    const client = getClient();
    try {
        const pulls = await client.repos.listPulls(options.owner, options.repo, {
            state: options.state || 'all',
        });
        console.log(JSON.stringify(pulls, null, 2));
    }
    catch (error) {
        console.error('Error listing pulls:', error);
        process.exit(1);
    }
}
export async function getPull(options) {
    const client = getClient();
    try {
        const pull = await client.repos.getPull(options.owner, options.repo, options.number);
        console.log(JSON.stringify(pull, null, 2));
    }
    catch (error) {
        console.error('Error getting pull:', error);
        process.exit(1);
    }
}
export async function createPull(options) {
    const client = getClient();
    try {
        const pull = await client.pulls.create(options.owner, options.repo, {
            title: options.title,
            head: options.head,
            base: options.base,
            body: options.body || '',
        });
        console.log(JSON.stringify(pull, null, 2));
    }
    catch (error) {
        console.error('Error creating pull:', error);
        process.exit(1);
    }
}
export async function listPullCommits(options) {
    const client = getClient();
    try {
        const commits = await client.pulls.listCommits(options.owner, options.repo, options.number);
        console.log(JSON.stringify(commits, null, 2));
    }
    catch (error) {
        console.error('Error listing pull commits:', error);
        process.exit(1);
    }
}
export async function listPullFiles(options) {
    const client = getClient();
    try {
        const files = await client.pulls.listFiles(options.owner, options.repo, options.number);
        console.log(JSON.stringify(files, null, 2));
    }
    catch (error) {
        console.error('Error listing pull files:', error);
        process.exit(1);
    }
}
