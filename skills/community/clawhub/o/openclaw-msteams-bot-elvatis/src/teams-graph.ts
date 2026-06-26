/**
 * OpenClaw Skill: teams-graph
 * Microsoft Graph API - Teams file access and team/channel listing.
 *
 * Required Azure AD App permissions (Application):
 *   - Files.ReadWrite.All
 *   - Sites.ReadWrite.All
 *   - Team.ReadBasic.All
 *   - Channel.ReadBasic.All
 *
 * Authentication: Client credentials flow via @azure/msal-node
 * API calls: Native fetch (Node 18+)
 * Graph API base: https://graph.microsoft.com/v1.0/
 */

import { ConfidentialClientApplication } from '@azure/msal-node'
import type { GraphConfig, DriveItem, Team, Channel, ToolResult } from './types'

const GRAPH_BASE = 'https://graph.microsoft.com/v1.0'
const GRAPH_SCOPE = 'https://graph.microsoft.com/.default'

const TEXT_EXTENSIONS = new Set(['.txt', '.md', '.csv', '.json', '.xml', '.html', '.htm', '.yaml', '.yml', '.log', '.ini', '.cfg', '.conf', '.sh', '.bat', '.ps1', '.ts', '.js', '.py', '.java', '.cs', '.go', '.rb', '.rs', '.sql'])

class GraphClient {
  private msalApp: ConfidentialClientApplication
  private tokenCache: { token: string; expiresAt: number } | null = null

  constructor(private config: GraphConfig) {
    this.msalApp = new ConfidentialClientApplication({
      auth: {
        clientId: config.clientId,
        authority: `https://login.microsoftonline.com/${config.tenantId}`,
        clientSecret: config.clientSecret,
      },
    })
  }

  private async getToken(): Promise<string> {
    const now = Date.now()
    if (this.tokenCache && this.tokenCache.expiresAt > now + 60_000) {
      return this.tokenCache.token
    }

    const result = await this.msalApp.acquireTokenByClientCredential({
      scopes: [GRAPH_SCOPE],
    })

    if (!result || !result.accessToken) {
      throw new Error('Failed to acquire access token from Azure AD')
    }

    this.tokenCache = {
      token: result.accessToken,
      expiresAt: now + (result.expiresOn ? result.expiresOn.getTime() - now : 3600_000),
    }

    return this.tokenCache.token
  }

  private async graphFetch(path: string, options: RequestInit = {}): Promise<Response> {
    const token = await this.getToken()
    const url = path.startsWith('http') ? path : `${GRAPH_BASE}${path}`

    const response = await fetch(url, {
      ...options,
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    if (!response.ok) {
      const body = await response.text().catch(() => '')
      throw new Error(`Graph API ${response.status} ${response.statusText}: ${body}`)
    }

    return response
  }

  private async graphJson<T>(path: string, options: RequestInit = {}): Promise<T> {
    const response = await this.graphFetch(path, options)
    return response.json() as Promise<T>
  }

  async listTeams(): Promise<Team[]> {
    const result = await this.graphJson<{ value: Team[] }>('/teams')
    return result.value
  }

  async listChannels(teamId: string): Promise<Channel[]> {
    const result = await this.graphJson<{ value: Channel[] }>(`/teams/${encodeURIComponent(teamId)}/channels`)
    return result.value
  }

  async listFiles(teamId: string, channelId: string): Promise<DriveItem[]> {
    const result = await this.graphJson<{ value: DriveItem[] }>(
      `/teams/${encodeURIComponent(teamId)}/channels/${encodeURIComponent(channelId)}/filesFolder/children`
    )
    return result.value
  }

  async readFile(driveId: string, itemId: string): Promise<{ name: string; mimeType: string; content: string; size: number }> {
    const meta = await this.graphJson<DriveItem>(
      `/drives/${encodeURIComponent(driveId)}/items/${encodeURIComponent(itemId)}`
    )

    const name = meta.name
    const ext = name.includes('.') ? `.${name.split('.').pop()!.toLowerCase()}` : ''
    const mimeType = meta.file?.mimeType ?? 'application/octet-stream'
    const size = meta.size

    let content: string

    if (TEXT_EXTENSIONS.has(ext) || mimeType.startsWith('text/')) {
      const response = await this.graphFetch(
        `/drives/${encodeURIComponent(driveId)}/items/${encodeURIComponent(itemId)}/content`
      )
      content = await response.text()
    } else if (ext === '.docx' || mimeType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
      // Extract plain text via Graph API content endpoint
      // For .docx, download raw and note it's binary
      content = await this.extractDocxText(driveId, itemId)
    } else if (ext === '.xlsx' || mimeType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
      content = await this.extractXlsxSummary(driveId, itemId)
    } else {
      content = `[Binary file: ${name} (${mimeType}, ${size} bytes). Use download URL to access.]`
    }

    return { name, mimeType, content, size }
  }

  private async extractDocxText(driveId: string, itemId: string): Promise<string> {
    // Use Graph API to get HTML content of the document, then strip tags
    try {
      const response = await this.graphFetch(
        `/drives/${encodeURIComponent(driveId)}/items/${encodeURIComponent(itemId)}/content?format=pdf`
      )
      // Fallback: just download as text and return what we get
      const text = await response.text()
      // Strip HTML tags if present
      return text.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim() || '[Empty document]'
    } catch {
      // If format conversion fails, try direct download
      try {
        const response = await this.graphFetch(
          `/drives/${encodeURIComponent(driveId)}/items/${encodeURIComponent(itemId)}/content`
        )
        const buffer = await response.arrayBuffer()
        return `[DOCX file: ${buffer.byteLength} bytes. Direct text extraction not available via Graph API. Consider downloading and processing locally.]`
      } catch (innerErr) {
        const message = innerErr instanceof Error ? innerErr.message : String(innerErr)
        return `[Failed to read DOCX content: ${message}]`
      }
    }
  }

  private async extractXlsxSummary(driveId: string, itemId: string): Promise<string> {
    // Use Graph API workbook sessions to read worksheet names and a data preview
    try {
      const worksheets = await this.graphJson<{ value: Array<{ id: string; name: string; position: number }> }>(
        `/drives/${encodeURIComponent(driveId)}/items/${encodeURIComponent(itemId)}/workbook/worksheets`
      )

      const lines: string[] = [`Worksheets (${worksheets.value.length}):`]

      for (const ws of worksheets.value.slice(0, 5)) {
        lines.push(`  - ${ws.name}`)

        try {
          const range = await this.graphJson<{ text: string[][] }>(
            `/drives/${encodeURIComponent(driveId)}/items/${encodeURIComponent(itemId)}/workbook/worksheets/${encodeURIComponent(ws.id)}/usedRange?$select=text`,
          )

          if (range.text && range.text.length > 0) {
            const previewRows = range.text.slice(0, 10)
            for (const row of previewRows) {
              lines.push(`    | ${row.join(' | ')} |`)
            }
            if (range.text.length > 10) {
              lines.push(`    ... (${range.text.length - 10} more rows)`)
            }
          }
        } catch {
          lines.push('    [Could not read worksheet data]')
        }
      }

      if (worksheets.value.length > 5) {
        lines.push(`  ... and ${worksheets.value.length - 5} more worksheets`)
      }

      return lines.join('\n')
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err)
      return `[Failed to read XLSX summary: ${message}]`
    }
  }

  async writeFile(
    driveId: string,
    parentItemId: string,
    filename: string,
    content: string
  ): Promise<DriveItem> {
    // For files up to 4MB, use simple upload
    const contentBuffer = Buffer.from(content, 'utf-8')

    if (contentBuffer.byteLength > 4 * 1024 * 1024) {
      return this.writeFileLargeUpload(driveId, parentItemId, filename, contentBuffer)
    }

    const result = await this.graphJson<DriveItem>(
      `/drives/${encodeURIComponent(driveId)}/items/${encodeURIComponent(parentItemId)}:/${encodeURIComponent(filename)}:/content`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/octet-stream' },
        body: contentBuffer,
      }
    )

    return result
  }

  private async writeFileLargeUpload(
    driveId: string,
    parentItemId: string,
    filename: string,
    content: Buffer
  ): Promise<DriveItem> {
    // Create upload session for files > 4MB
    const session = await this.graphJson<{ uploadUrl: string }>(
      `/drives/${encodeURIComponent(driveId)}/items/${encodeURIComponent(parentItemId)}:/${encodeURIComponent(filename)}:/createUploadSession`,
      {
        method: 'POST',
        body: JSON.stringify({
          item: { '@microsoft.graph.conflictBehavior': 'replace', name: filename },
        }),
      }
    )

    const chunkSize = 3_276_800 // 3.125 MB (must be multiple of 320 KB)
    let offset = 0
    let result: DriveItem | null = null

    while (offset < content.byteLength) {
      const end = Math.min(offset + chunkSize, content.byteLength)
      const chunk = content.subarray(offset, end)
      const token = await this.getToken()

      const response = await fetch(session.uploadUrl, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Length': chunk.byteLength.toString(),
          'Content-Range': `bytes ${offset}-${end - 1}/${content.byteLength}`,
        },
        body: chunk,
      })

      if (!response.ok) {
        const body = await response.text().catch(() => '')
        throw new Error(`Upload chunk failed at offset ${offset}: ${response.status} ${body}`)
      }

      if (response.status === 200 || response.status === 201) {
        result = (await response.json()) as DriveItem
      }

      offset = end
    }

    if (!result) {
      throw new Error('Upload completed but no item metadata returned')
    }

    return result
  }
}

// --- OpenClaw Skill Export ---

let clientInstance: GraphClient | null = null

function getClient(config: GraphConfig): GraphClient {
  if (!clientInstance) {
    clientInstance = new GraphClient(config)
  }
  return clientInstance
}

function validateConfig(config: unknown): GraphConfig {
  const cfg = config as Record<string, unknown>
  if (!cfg || typeof cfg.tenantId !== 'string' || !cfg.tenantId) {
    throw new Error('Missing required config: tenantId')
  }
  if (typeof cfg.clientId !== 'string' || !cfg.clientId) {
    throw new Error('Missing required config: clientId')
  }
  if (typeof cfg.clientSecret !== 'string' || !cfg.clientSecret) {
    throw new Error('Missing required config: clientSecret')
  }
  return { tenantId: cfg.tenantId, clientId: cfg.clientId, clientSecret: cfg.clientSecret }
}

function ok(data: unknown): ToolResult {
  return { success: true, data }
}

function fail(error: unknown): ToolResult {
  const message = error instanceof Error ? error.message : String(error)
  return { success: false, error: message }
}

export async function teams_list_teams(config: unknown): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    const client = getClient(cfg)
    const teams = await client.listTeams()
    return ok(teams.map(t => ({ id: t.id, displayName: t.displayName, description: t.description })))
  } catch (err) {
    return fail(err)
  }
}

export async function teams_list_channels(
  config: unknown,
  params: { teamId: string }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    if (!params?.teamId) throw new Error('Missing required parameter: teamId')
    const client = getClient(cfg)
    const channels = await client.listChannels(params.teamId)
    return ok(channels.map(c => ({ id: c.id, displayName: c.displayName, description: c.description, membershipType: c.membershipType })))
  } catch (err) {
    return fail(err)
  }
}

export async function teams_list_files(
  config: unknown,
  params: { teamId: string; channelId: string }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    if (!params?.teamId) throw new Error('Missing required parameter: teamId')
    if (!params?.channelId) throw new Error('Missing required parameter: channelId')
    const client = getClient(cfg)
    const files = await client.listFiles(params.teamId, params.channelId)
    return ok(files.map(f => ({
      id: f.id,
      name: f.name,
      size: f.size,
      webUrl: f.webUrl,
      lastModified: f.lastModifiedDateTime,
      isFolder: !!f.folder,
      driveId: f.parentReference?.driveId,
      parentId: f.parentReference?.id,
    })))
  } catch (err) {
    return fail(err)
  }
}

export async function teams_read_file(
  config: unknown,
  params: { driveId: string; itemId: string }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    if (!params?.driveId) throw new Error('Missing required parameter: driveId')
    if (!params?.itemId) throw new Error('Missing required parameter: itemId')
    const client = getClient(cfg)
    const result = await client.readFile(params.driveId, params.itemId)
    return ok(result)
  } catch (err) {
    return fail(err)
  }
}

export async function teams_write_file(
  config: unknown,
  params: { driveId: string; parentItemId: string; filename: string; content: string }
): Promise<ToolResult> {
  try {
    const cfg = validateConfig(config)
    if (!params?.driveId) throw new Error('Missing required parameter: driveId')
    if (!params?.parentItemId) throw new Error('Missing required parameter: parentItemId')
    if (!params?.filename) throw new Error('Missing required parameter: filename')
    if (typeof params?.content !== 'string') throw new Error('Missing required parameter: content')
    const client = getClient(cfg)
    const item = await client.writeFile(params.driveId, params.parentItemId, params.filename, params.content)
    return ok({ id: item.id, name: item.name, size: item.size, webUrl: item.webUrl })
  } catch (err) {
    return fail(err)
  }
}

export const teamsGraphSkill = {
  name: 'teams-graph',
  description: 'Microsoft Graph API integration for Teams file access and team/channel listing',
  tools: {
    teams_list_teams: {
      description: 'List all teams the bot has access to',
      parameters: {},
      execute: teams_list_teams,
    },
    teams_list_channels: {
      description: 'List channels in a team',
      parameters: {
        teamId: { type: 'string', required: true, description: 'The team ID' },
      },
      execute: teams_list_channels,
    },
    teams_list_files: {
      description: 'List files in a Teams channel folder',
      parameters: {
        teamId: { type: 'string', required: true, description: 'The team ID' },
        channelId: { type: 'string', required: true, description: 'The channel ID' },
      },
      execute: teams_list_files,
    },
    teams_read_file: {
      description: 'Read file content from a Teams drive (supports .txt, .md, .docx text, .xlsx summary)',
      parameters: {
        driveId: { type: 'string', required: true, description: 'The drive ID' },
        itemId: { type: 'string', required: true, description: 'The item ID' },
      },
      execute: teams_read_file,
    },
    teams_write_file: {
      description: 'Write/upload a file to a Teams channel folder',
      parameters: {
        driveId: { type: 'string', required: true, description: 'The drive ID' },
        parentItemId: { type: 'string', required: true, description: 'The parent folder item ID' },
        filename: { type: 'string', required: true, description: 'The filename to create/overwrite' },
        content: { type: 'string', required: true, description: 'The file content (UTF-8 text)' },
      },
      execute: teams_write_file,
    },
  },
}

export default teamsGraphSkill
