import { McpServer } from '@modelcontextprotocol/server';
import { z } from 'zod';
import { accountParam, runOrDiagnose, pageTokenParam, pageAliasParam, resolvePageToken, pos, confinePath, confirmTokenParam, requireDispatchConfirmation } from '../../../gogcli-mcp/src/lib.js';
import type { GogArg } from '../../../gogcli-mcp/src/lib.js';

// People is the richer API behind Google Contacts: Workspace directory
// search, profile fields, and relations.
export function registerExtraContactsTools(server: McpServer): void {
  server.registerTool('gog_people_me', {
    description: 'Show your own People profile (people/me).',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      account: accountParam,
    }),
  }, async ({ account }) => {
    return runOrDiagnose(['people', 'me'], { account });
  });

  server.registerTool('gog_people_get', {
    description: 'Get a People profile by resource name.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      userId: z.string().describe('Person resource name (people/...) or email'),
      account: accountParam,
    }),
  }, async ({ userId, account }) => {
    return runOrDiagnose(['people', 'get', pos(userId)], { account });
  });

  server.registerTool('gog_people_search', {
    description: 'Search the Google Workspace directory (covers internal users, unlike contacts search which is limited to your personal contacts).',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      query: z.string().describe('Search query (name, email, etc.)'),
      max: z.number().optional().describe('Max results (default: 50)'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      all: z.boolean().optional().describe('Fetch all pages'),
      account: accountParam,
    }),
  }, async ({ query, max, pageToken, page, all, account }) => {
    const args: GogArg[] = ['people', 'search', pos(query)];
    if (max !== undefined) args.push(`--max=${max}`);
    const token = resolvePageToken({ pageToken, page });
    if (token) args.push(`--page=${token}`);
    if (all) args.push('--all');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_people_relations', {
    description: 'Get relations (manager, reports, etc.) for a user. Defaults to self when userId is omitted.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      userId: z.string().optional().describe('Person resource name (defaults to self when omitted)'),
      type: z.string().optional().describe('Filter to a specific relation type (e.g. "manager")'),
      account: accountParam,
    }),
  }, async ({ userId, type, account }) => {
    const args: GogArg[] = ['people', 'relations'];
    if (userId) args.push(pos(userId));
    if (type) args.push(`--type=${type}`);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_contacts_update', {
    description: 'Update an existing Google Contact. Empty string clears a field; repeatable fields (url/address/custom/relation) take comma/semicolon-separated lists.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      resourceName: z.string().describe('Contact resource name (people/...)'),
      given: z.string().optional().describe('Given (first) name'),
      family: z.string().optional().describe('Family (last) name'),
      email: z.string().optional().describe('Email address (empty string clears)'),
      phone: z.string().optional().describe('Phone number (empty string clears)'),
      org: z.string().optional().describe('Organization/company name (empty string clears)'),
      title: z.string().optional().describe('Job title (empty string clears)'),
      url: z.string().optional().describe('URL(s), comma-separated (empty string clears all)'),
      note: z.string().optional().describe('Note/biography (empty string clears)'),
      address: z.string().optional().describe('Postal address(es), semicolon-separated (empty string clears all)'),
      birthday: z.string().optional().describe('Birthday in YYYY-MM-DD (empty string clears)'),
      ignoreEtag: z.boolean().optional().describe('Allow update even if a supplied etag is stale (may overwrite concurrent changes)'),
      account: accountParam,
    }),
  }, async ({ resourceName, given, family, email, phone, org, title, url, note, address, birthday, ignoreEtag, account }) => {
    const args: GogArg[] = ['contacts', 'update', pos(resourceName)];
    if (given !== undefined) args.push(`--given=${given}`);
    if (family !== undefined) args.push(`--family=${family}`);
    if (email !== undefined) args.push(`--email=${email}`);
    if (phone !== undefined) args.push(`--phone=${phone}`);
    if (org !== undefined) args.push(`--org=${org}`);
    if (title !== undefined) args.push(`--title=${title}`);
    if (url !== undefined) args.push(`--url=${url}`);
    if (note !== undefined) args.push(`--note=${note}`);
    if (address !== undefined) args.push(`--address=${address}`);
    if (birthday !== undefined) args.push(`--birthday=${birthday}`);
    if (ignoreEtag) args.push('--ignore-etag');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_contacts_delete', {
    description: 'Delete a Google Contact by resource name.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      resourceName: z.string().describe('Contact resource name (people/...)'),
      account: accountParam,
    }),
  }, async ({ resourceName, account }) => {
    return runOrDiagnose(['contacts', 'delete', pos(resourceName), '--force'], { account }); // gog gates this op; without --force the runner's --no-input makes it refuse
  });

  server.registerTool('gog_contacts_batch_get', {
    description: 'Fetch exact Google Contacts by People resource name in native API batches (up to 200).',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({ resourceNames: z.array(z.string().min(1)).min(1).max(200).describe('Exact resource names such as people/c123; maximum 200'), account: accountParam }),
  }, async ({ resourceNames, account }) => runOrDiagnose(['contacts', 'batch', 'get', ...resourceNames.map(pos)], { account }));

  server.registerTool('gog_contacts_batch_create', {
    description: 'Create Google Contacts in native People API batches (up to 200). peopleJson is a JSON array of People API Person resources. The payload is materialized in a temporary file on the gog host.',
    // Same kind of write as gog_contacts_create, so the same annotation.
    annotations: { readOnlyHint: false, destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({ peopleJson: z.string().describe('JSON array of People API Person resources, up to 200 contacts'), account: accountParam }),
  }, async ({ peopleJson, account }) => {
    let people: unknown;
    try { people = JSON.parse(peopleJson); } catch { throw new Error('peopleJson must be valid JSON'); }
    if (!Array.isArray(people) || people.length === 0 || people.length > 200) throw new Error('peopleJson must be a non-empty array with at most 200 contacts');
    return runOrDiagnose(['contacts', 'batch', 'create', { kind: 'file', flag: 'from-file', contents: peopleJson, ext: 'json' }], { account });
  });

  server.registerTool('gog_contacts_batch_update', {
    description: 'Update Google Contacts in native People API batches. peopleByResourceName is a JSON object keyed by People resource name; each value must include the CONTACT source metadata and etag returned by a prior read. gog preserves those etag guards and reports partial progress.',
    // Overwrites fields like gog_contacts_update, so the same annotation.
    annotations: { readOnlyHint: false, destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({ peopleByResourceName: z.string().describe('JSON object keyed by people/... resource name, with Person resources including CONTACT source metadata and etag'), account: accountParam }),
  }, async ({ peopleByResourceName, account }) => {
    let people: unknown;
    try { people = JSON.parse(peopleByResourceName); } catch { throw new Error('peopleByResourceName must be valid JSON'); }
    if (!people || typeof people !== 'object' || Array.isArray(people) || Object.keys(people).length === 0 || Object.keys(people).length > 200) throw new Error('peopleByResourceName must be a JSON object with between 1 and 200 contacts');
    return runOrDiagnose(['contacts', 'batch', 'update', { kind: 'file', flag: 'from-file', contents: peopleByResourceName, ext: 'json' }], { account });
  });

  server.registerTool('gog_contacts_batch_delete', {
    description: 'Permanently delete exact Google Contacts in native People API batches (up to 500). Requires explicit user confirmation; deleted contacts cannot be restored from Trash.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({ resourceNames: z.array(z.string().min(1)).min(1).max(500).describe('Exact People resource names; maximum 500'), account: accountParam, confirmToken: confirmTokenParam }),
  }, async ({ resourceNames, account, confirmToken }, ctx) => {
    const confirmation = await requireDispatchConfirmation(ctx, {
      action: 'contacts.batch-delete',
      message: 'Review and confirm permanent deletion of these Google Contacts:',
      confirmationLabel: 'Confirm permanent deletion of the listed contacts.',
      details: { resourceNames },
      fallback: { args: { resourceNames, account }, tool: 'gog_contacts_batch_delete', account, confirmToken, subject: () => ({ target: 'contacts', payload: { resourceNames }, preview: { resourceNames } }) },
    });
    if (confirmation) return confirmation;
    return runOrDiagnose(['contacts', 'batch', 'delete', ...resourceNames.map(pos), '--force'], { account });
  });

  server.registerTool('gog_contacts_export', {
    description: 'Export contacts as vCard (.vcf). Provide a selector (resource name, email, or name), or use query / all to export multiple.',
    // Writes a file on the gog host and can overwrite one: not read-only (audit SEC-4).
    annotations: { readOnlyHint: false, destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      selector: z.string().optional().describe('Contact resource name (people/...), email, or name'),
      query: z.string().optional().describe('Search query to export (max 30 results)'),
      all: z.boolean().optional().describe('Export all personal contacts'),
      out: z.string().optional().describe('Output path (.vcf), or - for stdout (default: stdout)'),
      max: z.number().optional().describe('Max results for query (1-30)'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      account: accountParam,
    }),
  }, async ({ selector, query, all, out, max, pageToken, page, account }) => {
    if (out) confinePath(out, 'out', { allowDash: true });
    const args: GogArg[] = ['contacts', 'export'];
    if (selector) args.push(pos(selector));
    if (query) args.push(`--query=${query}`);
    if (all) args.push('--all');
    if (out) args.push(`--out=${out}`);
    if (max !== undefined) args.push(`--max=${max}`);
    const token = resolvePageToken({ pageToken, page });
    if (token) args.push(`--page=${token}`);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_contacts_dedupe', {
    description: 'Find likely duplicate personal contacts. Defaults to a read-only preview of the merge plan; set apply to actually merge each duplicate group and delete the redundant contacts (etag-checked, with ambiguous or unmergeable groups refused). Scope a risky apply with resource. Always preview first.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      match: z.string().optional().describe('Match fields, comma-separated from email,phone,name (default: email,phone)'),
      max: z.number().optional().describe('Max contacts to scan (0 = all). Mutually exclusive with resource — gog rejects passing both.'),
      resource: z.array(z.string()).optional().describe('Limit dedupe to these exact contact resource names (e.g. people/c123), repeatable — useful to scope an apply to known duplicates. Mutually exclusive with max.'),
      apply: z.boolean().optional().describe('Merge each duplicate group and DELETE the redundant contacts. Without this the tool only previews the plan. Destructive — preview first.'),
      failEmpty: z.boolean().optional().describe('Exit with an error (code 3) when no duplicates are found, instead of succeeding empty.'),
      account: accountParam,
    }),
  }, async ({ match, max, resource, apply, failEmpty, account }) => {
    const args: GogArg[] = ['contacts', 'dedupe'];
    if (match) args.push(`--match=${match}`);
    if (max !== undefined) args.push(`--max=${max}`);
    if (resource) for (const r of resource) args.push(`--resource=${r}`);
    if (apply) args.push('--apply');
    if (failEmpty) args.push('--fail-empty');
    if (apply) args.push('--force'); // gog gates this op; without --force the runner's --no-input makes it refuse
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_contacts_directory_list', {
    description: 'List people from the Google Workspace directory (domain shared contacts).',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      max: z.number().optional().describe('Max results (default: 50)'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      all: z.boolean().optional().describe('Fetch all pages'),
      account: accountParam,
    }),
  }, async ({ max, pageToken, page, all, account }) => {
    const args: GogArg[] = ['contacts', 'directory', 'list'];
    if (max !== undefined) args.push(`--max=${max}`);
    const token = resolvePageToken({ pageToken, page });
    if (token) args.push(`--page=${token}`);
    if (all) args.push('--all');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_contacts_other_list', {
    description: 'List "other contacts" — auto-collected addresses (e.g. people you have emailed) that are not in your saved contacts.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      max: z.number().optional().describe('Max results (default: 100)'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      all: z.boolean().optional().describe('Fetch all pages'),
      account: accountParam,
    }),
  }, async ({ max, pageToken, page, all, account }) => {
    const args: GogArg[] = ['contacts', 'other', 'list'];
    if (max !== undefined) args.push(`--max=${max}`);
    const token = resolvePageToken({ pageToken, page });
    if (token) args.push(`--page=${token}`);
    if (all) args.push('--all');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_contacts_other_search', {
    description: 'Search "other contacts" — auto-collected addresses not in your saved contacts.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      query: z.string().describe('Search query'),
      max: z.number().optional().describe('Max results (default: 50)'),
      account: accountParam,
    }),
  }, async ({ query, max, account }) => {
    const args: GogArg[] = ['contacts', 'other', 'search', pos(query)];
    if (max !== undefined) args.push(`--max=${max}`);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_people_raw', {
    description: 'Dump the raw People API response as JSON (lossless; for scripting and LLM consumption).',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      userId: z.string().describe('Person resource name (people/...) or email'),
      personFields: z.string().optional().describe('People API personFields mask (default: broad set)'),
      pretty: z.boolean().optional().describe('Pretty-print JSON (default: compact single-line)'),
      account: accountParam,
    }),
  }, async ({ userId, personFields, pretty, account }) => {
    const args: GogArg[] = ['people', 'raw', pos(userId)];
    if (personFields) args.push(`--person-fields=${personFields}`);
    if (pretty) args.push('--pretty');
    // Verbatim by contract: see the `lossless` note on runOrDiagnose.
    return runOrDiagnose(args, { account, lossless: true });
  });
}
