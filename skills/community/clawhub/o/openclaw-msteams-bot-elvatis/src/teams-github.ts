/**
 * OpenClaw Skill: teams-github
 * GitHub integration for Teams: repo, file, issue, and PR management.
 *
 * Authentication:
 *   Option A: GitHub App (appId, privateKey, installationId)
 *   Option B: Personal Access Token (token)
 *
 * Uses @octokit/rest for API calls.
 */

import { Octokit } from '@octokit/rest'
import { createAppAuth } from '@octokit/auth-app'
import type { GitHubConfig, ToolResult } from './types'

let octokitInstance: Octokit | null = null
let lastConfigHash: string | null = null

function configHash(config: GitHubConfig): string {
  return JSON.stringify({
    appId: config.appId,
    installationId: config.installationId,
    token: config.token,
  })
}

function getOctokit(config: GitHubConfig): Octokit {
  const hash = configHash(config)
  if (octokitInstance && lastConfigHash === hash) {
    return octokitInstance
  }

  if (config.appId && config.privateKey && config.installationId) {
    octokitInstance = new Octokit({
      authStrategy: createAppAuth,
      auth: {
        appId: config.appId,
        privateKey: config.privateKey,
        installationId: config.installationId,
      },
    })
  } else if (config.token) {
    octokitInstance = new Octokit({ auth: config.token })
  } else {
    throw new Error('GitHub config requires either (appId + privateKey + installationId) or token')
  }

  lastConfigHash = hash
  return octokitInstance
}

function validateConfig(config: unknown): GitHubConfig {
  const cfg = config as Record<string, unknown>
  if (!cfg) throw new Error('Missing GitHub config')

  const hasApp = cfg.appId && cfg.privateKey && cfg.installationId
  const hasToken = cfg.token && typeof cfg.token === 'string'

  if (!hasApp && !hasToken) {
    throw new Error('GitHub config requires either (appId + privateKey + installationId) or token')
  }

  return {
    appId: typeof cfg.appId === 'number' ? cfg.appId : undefined,
    privateKey: typeof cfg.privateKey === 'string' ? cfg.privateKey : undefined,
    installationId: typeof cfg.installationId === 'number' ? cfg.installationId : undefined,
    token: typeof cfg.token === 'string' ? cfg.token : undefined,
    defaultOrg: typeof cfg.defaultOrg === 'string' ? cfg.defaultOrg : undefined,
  }
}

function ok(data: unknown): ToolResult {
  return { success: true, data }
}

function fail(error: unknown): ToolResult {
  const message = error instanceof Error ? error.message : String(error)
  return { success: false, error: message }
}

export async function github_list_repos(
  config: unknown,
  params: { org?: string }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    const octokit = getOctokit(cfg)
    const org = params?.org || cfg.defaultOrg

    let repos
    if (org) {
      const response = await octokit.repos.listForOrg({
        org,
        per_page: 100,
        sort: 'updated',
        direction: 'desc',
      })
      repos = response.data
    } else {
      const response = await octokit.repos.listForAuthenticatedUser({
        per_page: 100,
        sort: 'updated',
        direction: 'desc',
      })
      repos = response.data
    }

    return ok(repos.map(r => ({
      name: r.name,
      fullName: r.full_name,
      description: r.description,
      private: r.private,
      defaultBranch: r.default_branch,
      language: r.language,
      updatedAt: r.updated_at,
      htmlUrl: r.html_url,
    })))
  } catch (err) {
    return fail(err)
  }
}

export async function github_read_file(
  config: unknown,
  params: { owner: string; repo: string; path: string; ref?: string }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    const octokit = getOctokit(cfg)

    if (!params?.owner) throw new Error('Missing required parameter: owner')
    if (!params?.repo) throw new Error('Missing required parameter: repo')
    if (!params?.path) throw new Error('Missing required parameter: path')

    const response = await octokit.repos.getContent({
      owner: params.owner,
      repo: params.repo,
      path: params.path,
      ref: params.ref,
    })

    const data = response.data
    if (Array.isArray(data)) {
      // It's a directory listing
      return ok(data.map(item => ({
        name: item.name,
        path: item.path,
        type: item.type,
        size: item.size,
        sha: item.sha,
      })))
    }

    if (data.type === 'file' && 'content' in data && data.content) {
      const content = Buffer.from(data.content, 'base64').toString('utf-8')
      return ok({
        name: data.name,
        path: data.path,
        size: data.size,
        sha: data.sha,
        encoding: 'utf-8',
        content,
      })
    }

    if (data.type === 'symlink' && 'target' in data) {
      return ok({ name: data.name, path: data.path, type: 'symlink', target: data.target })
    }

    if (data.type === 'submodule' && 'submodule_git_url' in data) {
      return ok({ name: data.name, path: data.path, type: 'submodule', submoduleUrl: data.submodule_git_url })
    }

    return ok({ name: data.name, path: data.path, type: data.type, size: data.size })
  } catch (err) {
    return fail(err)
  }
}

export async function github_write_file(
  config: unknown,
  params: { owner: string; repo: string; path: string; content: string; message: string; branch?: string }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    const octokit = getOctokit(cfg)

    if (!params?.owner) throw new Error('Missing required parameter: owner')
    if (!params?.repo) throw new Error('Missing required parameter: repo')
    if (!params?.path) throw new Error('Missing required parameter: path')
    if (typeof params?.content !== 'string') throw new Error('Missing required parameter: content')
    if (!params?.message) throw new Error('Missing required parameter: message')

    // Check if file exists to get its SHA (required for updates)
    let existingSha: string | undefined
    try {
      const existing = await octokit.repos.getContent({
        owner: params.owner,
        repo: params.repo,
        path: params.path,
        ref: params.branch,
      })
      if (!Array.isArray(existing.data) && 'sha' in existing.data) {
        existingSha = existing.data.sha
      }
    } catch (err: unknown) {
      // 404 means file doesn't exist yet, which is fine for creation
      const status = (err as { status?: number })?.status
      if (status !== 404) throw err
    }

    const response = await octokit.repos.createOrUpdateFileContents({
      owner: params.owner,
      repo: params.repo,
      path: params.path,
      message: params.message,
      content: Buffer.from(params.content, 'utf-8').toString('base64'),
      branch: params.branch,
      sha: existingSha,
    })

    return ok({
      path: response.data.content?.path,
      sha: response.data.content?.sha,
      size: response.data.content?.size,
      commitSha: response.data.commit.sha,
      commitMessage: response.data.commit.message,
      htmlUrl: response.data.content?.html_url,
    })
  } catch (err) {
    return fail(err)
  }
}

export async function github_list_issues(
  config: unknown,
  params: { owner: string; repo: string; state?: 'open' | 'closed' | 'all' }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    const octokit = getOctokit(cfg)

    if (!params?.owner) throw new Error('Missing required parameter: owner')
    if (!params?.repo) throw new Error('Missing required parameter: repo')

    const response = await octokit.issues.listForRepo({
      owner: params.owner,
      repo: params.repo,
      state: params.state || 'open',
      per_page: 100,
      sort: 'updated',
      direction: 'desc',
    })

    // Filter out pull requests (GitHub API returns PRs as issues)
    const issues = response.data.filter(i => !i.pull_request)

    return ok(issues.map(i => ({
      number: i.number,
      title: i.title,
      state: i.state,
      labels: i.labels.map(l => (typeof l === 'string' ? l : l.name)),
      author: i.user?.login,
      assignees: i.assignees?.map(a => a.login),
      createdAt: i.created_at,
      updatedAt: i.updated_at,
      commentsCount: i.comments,
      htmlUrl: i.html_url,
    })))
  } catch (err) {
    return fail(err)
  }
}

export async function github_create_issue(
  config: unknown,
  params: { owner: string; repo: string; title: string; body: string; labels?: string[] }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    const octokit = getOctokit(cfg)

    if (!params?.owner) throw new Error('Missing required parameter: owner')
    if (!params?.repo) throw new Error('Missing required parameter: repo')
    if (!params?.title) throw new Error('Missing required parameter: title')
    if (!params?.body) throw new Error('Missing required parameter: body')

    const response = await octokit.issues.create({
      owner: params.owner,
      repo: params.repo,
      title: params.title,
      body: params.body,
      labels: params.labels,
    })

    return ok({
      number: response.data.number,
      title: response.data.title,
      state: response.data.state,
      htmlUrl: response.data.html_url,
      createdAt: response.data.created_at,
    })
  } catch (err) {
    return fail(err)
  }
}

export async function github_list_prs(
  config: unknown,
  params: { owner: string; repo: string; state?: 'open' | 'closed' | 'all' }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    const octokit = getOctokit(cfg)

    if (!params?.owner) throw new Error('Missing required parameter: owner')
    if (!params?.repo) throw new Error('Missing required parameter: repo')

    const response = await octokit.pulls.list({
      owner: params.owner,
      repo: params.repo,
      state: params.state || 'open',
      per_page: 100,
      sort: 'updated',
      direction: 'desc',
    })

    return ok(response.data.map(pr => ({
      number: pr.number,
      title: pr.title,
      state: pr.state,
      draft: pr.draft,
      author: pr.user?.login,
      baseBranch: pr.base.ref,
      headBranch: pr.head.ref,
      createdAt: pr.created_at,
      updatedAt: pr.updated_at,
      mergedAt: pr.merged_at,
      htmlUrl: pr.html_url,
      additions: (pr as any).additions,
      deletions: (pr as any).deletions,
      changedFiles: (pr as any).changed_files,
    })))
  } catch (err) {
    return fail(err)
  }
}

export async function github_get_pr(
  config: unknown,
  params: { owner: string; repo: string; prNumber: number }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    const octokit = getOctokit(cfg)

    if (!params?.owner) throw new Error('Missing required parameter: owner')
    if (!params?.repo) throw new Error('Missing required parameter: repo')
    if (!params?.prNumber) throw new Error('Missing required parameter: prNumber')

    const [prResponse, filesResponse] = await Promise.all([
      octokit.pulls.get({
        owner: params.owner,
        repo: params.repo,
        pull_number: params.prNumber,
      }),
      octokit.pulls.listFiles({
        owner: params.owner,
        repo: params.repo,
        pull_number: params.prNumber,
        per_page: 100,
      }),
    ])

    const pr = prResponse.data
    const files = filesResponse.data

    const diffSummary = files.map(f => ({
      filename: f.filename,
      status: f.status,
      additions: f.additions,
      deletions: f.deletions,
      changes: f.changes,
    }))

    return ok({
      number: pr.number,
      title: pr.title,
      state: pr.state,
      draft: pr.draft,
      body: pr.body,
      author: pr.user?.login,
      baseBranch: pr.base.ref,
      headBranch: pr.head.ref,
      mergeable: pr.mergeable,
      mergeableState: pr.mergeable_state,
      createdAt: pr.created_at,
      updatedAt: pr.updated_at,
      mergedAt: pr.merged_at,
      htmlUrl: pr.html_url,
      additions: (pr as any).additions,
      deletions: (pr as any).deletions,
      changedFiles: (pr as any).changed_files,
      commits: pr.commits,
      comments: pr.comments,
      reviewComments: pr.review_comments,
      diffSummary,
    })
  } catch (err) {
    return fail(err)
  }
}

export const teamsGithubSkill = {
  name: 'teams-github',
  description: 'GitHub integration for Teams: repo, file, issue, and PR management',
  tools: {
    github_list_repos: {
      description: 'List repositories (filtered to default org if configured)',
      parameters: {
        org: { type: 'string', required: false, description: 'Organization name (defaults to configured defaultOrg)' },
      },
      execute: github_list_repos,
    },
    github_read_file: {
      description: 'Read file content from a GitHub repository',
      parameters: {
        owner: { type: 'string', required: true, description: 'Repository owner' },
        repo: { type: 'string', required: true, description: 'Repository name' },
        path: { type: 'string', required: true, description: 'File path in the repo' },
        ref: { type: 'string', required: false, description: 'Git ref (branch, tag, or SHA)' },
      },
      execute: github_read_file,
    },
    github_write_file: {
      description: 'Create or update a file in a GitHub repository',
      parameters: {
        owner: { type: 'string', required: true, description: 'Repository owner' },
        repo: { type: 'string', required: true, description: 'Repository name' },
        path: { type: 'string', required: true, description: 'File path in the repo' },
        content: { type: 'string', required: true, description: 'File content (UTF-8 text)' },
        message: { type: 'string', required: true, description: 'Commit message' },
        branch: { type: 'string', required: false, description: 'Branch name (defaults to repo default branch)' },
      },
      execute: github_write_file,
    },
    github_list_issues: {
      description: 'List issues in a repository',
      parameters: {
        owner: { type: 'string', required: true, description: 'Repository owner' },
        repo: { type: 'string', required: true, description: 'Repository name' },
        state: { type: 'string', required: false, description: 'Filter by state: open, closed, all (default: open)' },
      },
      execute: github_list_issues,
    },
    github_create_issue: {
      description: 'Create a new issue in a repository',
      parameters: {
        owner: { type: 'string', required: true, description: 'Repository owner' },
        repo: { type: 'string', required: true, description: 'Repository name' },
        title: { type: 'string', required: true, description: 'Issue title' },
        body: { type: 'string', required: true, description: 'Issue body (Markdown)' },
        labels: { type: 'array', required: false, description: 'Labels to apply' },
      },
      execute: github_create_issue,
    },
    github_list_prs: {
      description: 'List pull requests in a repository',
      parameters: {
        owner: { type: 'string', required: true, description: 'Repository owner' },
        repo: { type: 'string', required: true, description: 'Repository name' },
        state: { type: 'string', required: false, description: 'Filter by state: open, closed, all (default: open)' },
      },
      execute: github_list_prs,
    },
    github_get_pr: {
      description: 'Get pull request details including diff summary',
      parameters: {
        owner: { type: 'string', required: true, description: 'Repository owner' },
        repo: { type: 'string', required: true, description: 'Repository name' },
        prNumber: { type: 'number', required: true, description: 'Pull request number' },
      },
      execute: github_get_pr,
    },
  },
}

export default teamsGithubSkill
