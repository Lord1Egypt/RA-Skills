import { getClient } from '../client.js';
export async function listIssues(options) {
    const client = getClient();
    try {
        const issues = await client.issues.list(options.owner, options.repo, {
            state: options.state || 'all',
        });
        console.log(JSON.stringify(issues, null, 2));
    }
    catch (error) {
        console.error('Error listing issues:', error);
        process.exit(1);
    }
}
export async function getIssue(options) {
    const client = getClient();
    try {
        const issue = await client.issues.get(options.owner, options.repo, options.number);
        console.log(JSON.stringify(issue, null, 2));
    }
    catch (error) {
        console.error('Error getting issue:', error);
        process.exit(1);
    }
}
export async function listComments(options) {
    const client = getClient();
    try {
        const comments = await client.issues.listComments(options.owner, options.repo, options.number);
        console.log(JSON.stringify(comments, null, 2));
    }
    catch (error) {
        console.error('Error listing comments:', error);
        process.exit(1);
    }
}
