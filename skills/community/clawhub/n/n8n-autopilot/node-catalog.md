# n8n Node Catalog & Credential Mapping

Quick reference for node types, their latest `typeVersion`, and the credential
key to use in the `credentials` block.

## Trigger Nodes

| Node Type | typeVersion | Credential Key |
|-----------|-------------|----------------|
| `n8n-nodes-base.manualTrigger` | 1 | — |
| `n8n-nodes-base.webhook` | 2 | `httpHeaderAuth` (optional) |
| `n8n-nodes-base.scheduleTrigger` | 1 | — |
| `n8n-nodes-base.formTrigger` | 1 | — |
| `n8n-nodes-base.emailimap` | 2 | `imap` |

## Logic & Transform Nodes

| Node Type | typeVersion | Credential Key |
|-----------|-------------|----------------|
| `n8n-nodes-base.code` | 2 | — |
| `n8n-nodes-base.set` | 3 | — |
| `n8n-nodes-base.if` | 2 | — |
| `n8n-nodes-base.switch` | 3 | — |
| `n8n-nodes-base.merge` | 3 | — |
| `n8n-nodes-base.splitInBatches` | 3 | — |
| `n8n-nodes-base.noOp` | 1 | — |
| `n8n-nodes-base.filter` | 1 | — |
| `n8n-nodes-base.sort` | 1 | — |
| `n8n-nodes-base.limit` | 1 | — |
| `n8n-nodes-base.removeDuplicates` | 1 | — |
| `n8n-nodes-base.splitOut` | 1 | — |
| `n8n-nodes-base.aggregate` | 1 | — |
| `n8n-nodes-base.xml` | 1 | — |
| `n8n-nodes-base.html` | 1 | — |
| `n8n-nodes-base.markdown` | 1 | — |
| `n8n-nodes-base.crypto` | 1 | — |
| `n8n-nodes-base.dateTime` | 2 | — |
| `n8n-nodes-base.wait` | 1 | — |
| `n8n-nodes-base.executeCommand` | 1 | — |
| `n8n-nodes-base.stopAndError` | 1 | — |
| `n8n-nodes-base.respondToWebhook` | 1 | — |
| `n8n-nodes-base.errorTrigger` | 1 | — |

## HTTP & Networking

| Node Type | typeVersion | Credential Key |
|-----------|-------------|----------------|
| `n8n-nodes-base.httpRequest` | 4 | varies (`httpHeaderAuth`, `httpBasicAuth`, `oAuth2Api`, etc.) |
| `n8n-nodes-base.graphql` | 1 | `httpHeaderAuth` |
| `n8n-nodes-base.ftp` | 1 | `ftp` |
| `n8n-nodes-base.ssh` | 1 | `sshPassword` or `sshPrivateKey` |

## Communication

| Node Type | typeVersion | Credential Key |
|-----------|-------------|----------------|
| `n8n-nodes-base.slack` | 2 | `slackApi` or `slackOAuth2Api` |
| `n8n-nodes-base.gmail` | 2 | `gmailOAuth2` |
| `n8n-nodes-base.emailSend` | 2 | `smtp` |
| `n8n-nodes-base.telegram` | 2 | `telegramApi` |
| `n8n-nodes-base.discord` | 2 | `discordApi` or `discordBotApi` |
| `n8n-nodes-base.mattermost` | 1 | `mattermostApi` |
| `n8n-nodes-base.whatsapp` | 1 | `whatsAppBusinessCloudApi` |

## Productivity & CRM

| Node Type | typeVersion | Credential Key |
|-----------|-------------|----------------|
| `n8n-nodes-base.googleSheets` | 4 | `googleSheetsOAuth2Api` |
| `n8n-nodes-base.googleDrive` | 3 | `googleDriveOAuth2Api` |
| `n8n-nodes-base.googleCalendar` | 1 | `googleCalendarOAuth2Api` |
| `n8n-nodes-base.notion` | 2 | `notionApi` |
| `n8n-nodes-base.airtable` | 2 | `airtableTokenApi` |
| `n8n-nodes-base.todoist` | 2 | `todoistApi` |
| `n8n-nodes-base.trello` | 1 | `trelloApi` |
| `n8n-nodes-base.asana` | 1 | `asanaApi` |
| `n8n-nodes-base.hubspot` | 2 | `hubspotApi` |
| `n8n-nodes-base.salesforce` | 1 | `salesforceOAuth2Api` |
| `n8n-nodes-base.pipedrive` | 1 | `pipedriveApi` |

## Databases

| Node Type | typeVersion | Credential Key |
|-----------|-------------|----------------|
| `n8n-nodes-base.postgres` | 2 | `postgres` |
| `n8n-nodes-base.mysql` | 2 | `mySql` |
| `n8n-nodes-base.mongodb` | 1 | `mongoDb` |
| `n8n-nodes-base.redis` | 1 | `redis` |
| `n8n-nodes-base.supabase` | 1 | `supabaseApi` |
| `n8n-nodes-base.elasticsearch` | 1 | `elasticsearchApi` |

## Payments & Commerce

| Node Type | typeVersion | Credential Key |
|-----------|-------------|----------------|
| `n8n-nodes-base.stripe` | 1 | `stripeApi` |
| `n8n-nodes-base.shopify` | 1 | `shopifyApi` |
| `n8n-nodes-base.woocommerce` | 1 | `wooCommerceApi` |
| `n8n-nodes-base.paypal` | 1 | `payPalApi` |

## Developer Tools

| Node Type | typeVersion | Credential Key |
|-----------|-------------|----------------|
| `n8n-nodes-base.github` | 1 | `githubApi` or `githubOAuth2Api` |
| `n8n-nodes-base.gitlab` | 1 | `gitlabApi` or `gitlabOAuth2Api` |
| `n8n-nodes-base.jira` | 1 | `jiraSoftwareCloudApi` |
| `n8n-nodes-base.linear` | 1 | `linearApi` |
| `n8n-nodes-base.jenkins` | 1 | `jenkinsApi` |

## AI / LLM

| Node Type | typeVersion | Credential Key |
|-----------|-------------|----------------|
| `@n8n/n8n-nodes-langchain.openAi` | 1 | `openAiApi` |
| `@n8n/n8n-nodes-langchain.lmChatOpenAi` | 1 | `openAiApi` |
| `@n8n/n8n-nodes-langchain.lmChatAnthropic` | 1 | `anthropicApi` |
| `@n8n/n8n-nodes-langchain.lmChatGoogleGemini` | 1 | `googleGeminiApi` |

## Sub-workflow

| Node Type | typeVersion | Credential Key |
|-----------|-------------|----------------|
| `n8n-nodes-base.executeWorkflow` | 1 | — |
| `n8n-nodes-base.executeWorkflowTrigger` | 1 | — |
