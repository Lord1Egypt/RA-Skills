import { describe, it, expect, vi, beforeEach } from 'vitest';
import { registerExtraContactsTools } from '../../src/tools/contacts-extra.js';
import * as lib from '../../../gogcli-mcp/src/lib.js';
import { createTestHarness, type TestHarness } from '@chrischall/mcp-utils/test';
import { rawTextResult } from '@chrischall/mcp-utils';
import { pos } from '../../../gogcli-mcp/src/argv.js';

vi.mock('../../../gogcli-mcp/src/lib.js', async (importOriginal) => {
  const actual = await importOriginal<typeof lib>();
  return {
    ...actual,
    runOrDiagnose: vi.fn(),
  };
});

let harness: TestHarness;

beforeEach(async () => {
  vi.clearAllMocks();
  vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{}'));
  harness = await createTestHarness(registerExtraContactsTools);
});

describe('gog_people_me', () => {
  it('calls runOrDiagnose with people me', async () => {
    await harness.callTool('gog_people_me', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['people', 'me'], { account: undefined });
  });

  it('forwards account', async () => {
    await harness.callTool('gog_people_me', { account: 'a@b.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['people', 'me'], { account: 'a@b.com' });
  });
});

describe('gog_people_get', () => {
  it('calls runOrDiagnose with userId', async () => {
    await harness.callTool('gog_people_get', { userId: 'people/c123' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['people', 'get', pos('people/c123')], { account: undefined });
  });
});

describe('gog_people_search', () => {
  it('calls runOrDiagnose with query', async () => {
    await harness.callTool('gog_people_search', { query: 'alice' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['people', 'search', pos('alice')], { account: undefined });
  });

  it('passes pagination flags', async () => {
    await harness.callTool('gog_people_search', { query: 'alice', max: 100, page: 'tok', all: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['people', 'search', pos('alice'), '--max=100', '--page=tok', '--all'],
      { account: undefined },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_people_search', { query: 'x', all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['people', 'search', pos('x')], { account: undefined });
  });
});

describe('gog_people_relations', () => {
  it('calls runOrDiagnose with no userId', async () => {
    await harness.callTool('gog_people_relations', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['people', 'relations'], { account: undefined });
  });

  it('passes userId and --type when provided', async () => {
    await harness.callTool('gog_people_relations', { userId: 'people/c123', type: 'manager' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['people', 'relations', pos('people/c123'), '--type=manager'],
      { account: undefined },
    );
  });
});

describe('gog_contacts_update', () => {
  it('calls runOrDiagnose with just resourceName', async () => {
    await harness.callTool('gog_contacts_update', { resourceName: 'people/c1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'update', pos('people/c1')], { account: undefined });
  });

  it('passes all fields including empty-string clears', async () => {
    await harness.callTool('gog_contacts_update', {
      resourceName: 'people/c1',
      given: 'Ada',
      family: 'Lovelace',
      email: '',
      phone: '+1',
      org: 'Analytical',
      title: 'Engineer',
      url: 'https://a.com',
      note: 'hi',
      address: '1 St;City',
      birthday: '1815-12-10',
      ignoreEtag: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'contacts', 'update', pos('people/c1'),
        '--given=Ada', '--family=Lovelace', '--email=', '--phone=+1',
        '--org=Analytical', '--title=Engineer', '--url=https://a.com',
        '--note=hi', '--address=1 St;City', '--birthday=1815-12-10', '--ignore-etag',
      ],
      { account: undefined },
    );
  });

  it('omits --ignore-etag when false', async () => {
    await harness.callTool('gog_contacts_update', { resourceName: 'people/c1', ignoreEtag: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'update', pos('people/c1')], { account: undefined });
  });
});

describe('gog_contacts_delete', () => {
  it('calls runOrDiagnose with resourceName', async () => {
    await harness.callTool('gog_contacts_delete', { resourceName: 'people/c1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'delete', pos('people/c1'), '--force'], { account: undefined });
  });
});

describe('native batched Contacts tools', () => {
  it('fetches exact resource names in one command', async () => {
    await harness.callTool('gog_contacts_batch_get', { resourceNames: ['people/a', 'people/b'] });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'batch', 'get', pos('people/a'), pos('people/b')], { account: undefined });
  });

  it('materializes a validated create array as a JSON file argument', async () => {
    const peopleJson = '[{"names":[{"givenName":"Ada"}]}]';
    await harness.callTool('gog_contacts_batch_create', { peopleJson });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith([
      'contacts', 'batch', 'create', { kind: 'file', flag: 'from-file', contents: peopleJson, ext: 'json' },
    ], { account: undefined });
  });

  it('rejects invalid create JSON before invoking gog', async () => {
    const result = await harness.callTool('gog_contacts_batch_create', { peopleJson: '{' });
    expect(result.isError).toBe(true);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('rejects an empty or non-array create payload', async () => {
    expect((await harness.callTool('gog_contacts_batch_create', { peopleJson: '{}' })).isError).toBe(true);
    expect((await harness.callTool('gog_contacts_batch_create', { peopleJson: '[]' })).isError).toBe(true);
    expect((await harness.callTool('gog_contacts_batch_create', { peopleJson: JSON.stringify(Array(201).fill({})) })).isError).toBe(true);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('materializes an update map and preserves the account', async () => {
    const peopleByResourceName = '{"people/a":{"etag":"x"}}';
    await harness.callTool('gog_contacts_batch_update', { peopleByResourceName, account: 'a@b.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith([
      'contacts', 'batch', 'update', { kind: 'file', flag: 'from-file', contents: peopleByResourceName, ext: 'json' },
    ], { account: 'a@b.com' });
  });

  it('rejects invalid or empty update maps', async () => {
    expect((await harness.callTool('gog_contacts_batch_update', { peopleByResourceName: '{' })).isError).toBe(true);
    expect((await harness.callTool('gog_contacts_batch_update', { peopleByResourceName: '[]' })).isError).toBe(true);
    expect((await harness.callTool('gog_contacts_batch_update', { peopleByResourceName: '{}' })).isError).toBe(true);
    const tooMany = Object.fromEntries(Array.from({ length: 201 }, (_, i) => [`people/${i}`, {}]));
    expect((await harness.callTool('gog_contacts_batch_update', { peopleByResourceName: JSON.stringify(tooMany) })).isError).toBe(true);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('requires confirmation and then forces the guarded permanent delete', async () => {
    const confirmed = await createTestHarness(registerExtraContactsTools, {
      elicitation: async () => ({ action: 'accept', content: { confirmed: true } }),
    });
    await confirmed.callTool('gog_contacts_batch_delete', { resourceNames: ['people/a', 'people/b'] });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith([
      'contacts', 'batch', 'delete', pos('people/a'), pos('people/b'), '--force',
    ], { account: undefined });
  });

  it('allows an unprompted client to confirm the exact batch with a one-time token', async () => {
    process.env.MCP_CONFIRM_MODE = 'ask-user';
    const unprompted = await createTestHarness(registerExtraContactsTools);
    const args = { resourceNames: ['people/a'] };
    const prompt = await unprompted.callTool('gog_contacts_batch_delete', args);
    const payload = JSON.parse(prompt.content[0].text);
    await unprompted.callTool('gog_contacts_batch_delete', { ...args, confirmToken: payload.confirmToken });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['contacts', 'batch', 'delete', pos('people/a'), '--force'], { account: undefined });
    delete process.env.MCP_CONFIRM_MODE;
  });
});

describe('gog_contacts_export', () => {
  it('calls runOrDiagnose with no options', async () => {
    await harness.callTool('gog_contacts_export', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'export'], { account: undefined });
  });

  it('passes selector and all flags', async () => {
    await harness.callTool('gog_contacts_export', {
      selector: 'people/c1',
      query: 'ada',
      all: true,
      out: 'out.vcf',
      max: 10,
      page: 'tok',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['contacts', 'export', pos('people/c1'), '--query=ada', '--all', '--out=out.vcf', '--max=10', '--page=tok'],
      { account: undefined },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_contacts_export', { all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'export'], { account: undefined });
  });
});

describe('gog_contacts_dedupe', () => {
  it('calls runOrDiagnose with no options', async () => {
    await harness.callTool('gog_contacts_dedupe', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'dedupe'], { account: undefined });
  });

  it('passes --match and --max', async () => {
    await harness.callTool('gog_contacts_dedupe', { match: 'name', max: 100 });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['contacts', 'dedupe', '--match=name', '--max=100'],
      { account: undefined },
    );
  });

  it('passes --apply, repeatable --resource, and --fail-empty', async () => {
    await harness.callTool('gog_contacts_dedupe', {
      apply: true,
      resource: ['people/c1', 'people/c2'],
      failEmpty: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['contacts', 'dedupe', '--resource=people/c1', '--resource=people/c2', '--apply', '--fail-empty', '--force'],
      { account: undefined },
    );
  });

  it('omits --apply and --fail-empty when false', async () => {
    await harness.callTool('gog_contacts_dedupe', { apply: false, failEmpty: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'dedupe'], { account: undefined });
  });
});

describe('gog_contacts_directory_list', () => {
  it('calls runOrDiagnose with no options', async () => {
    await harness.callTool('gog_contacts_directory_list', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'directory', 'list'], { account: undefined });
  });

  it('passes pagination flags', async () => {
    await harness.callTool('gog_contacts_directory_list', { max: 50, page: 'tok', all: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['contacts', 'directory', 'list', '--max=50', '--page=tok', '--all'],
      { account: undefined },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_contacts_directory_list', { all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'directory', 'list'], { account: undefined });
  });
});

describe('gog_contacts_other_list', () => {
  it('calls runOrDiagnose with no options', async () => {
    await harness.callTool('gog_contacts_other_list', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'other', 'list'], { account: undefined });
  });

  it('passes pagination flags', async () => {
    await harness.callTool('gog_contacts_other_list', { max: 100, page: 'tok', all: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['contacts', 'other', 'list', '--max=100', '--page=tok', '--all'],
      { account: undefined },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_contacts_other_list', { all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'other', 'list'], { account: undefined });
  });
});

describe('gog_contacts_other_search', () => {
  it('calls runOrDiagnose with query', async () => {
    await harness.callTool('gog_contacts_other_search', { query: 'ada' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['contacts', 'other', 'search', pos('ada')], { account: undefined });
  });

  it('passes --max when provided', async () => {
    await harness.callTool('gog_contacts_other_search', { query: 'ada', max: 25 });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['contacts', 'other', 'search', pos('ada'), '--max=25'],
      { account: undefined },
    );
  });
});

describe('gog_people_raw', () => {
  it('calls runOrDiagnose with userId', async () => {
    await harness.callTool('gog_people_raw', { userId: 'people/c123' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['people', 'raw', pos('people/c123')], { account: undefined, lossless: true });
  });

  it('passes --person-fields and --pretty when provided', async () => {
    await harness.callTool('gog_people_raw', {
      userId: 'people/c123',
      personFields: 'names,emailAddresses',
      pretty: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['people', 'raw', pos('people/c123'), '--person-fields=names,emailAddresses', '--pretty'],
      { account: undefined, lossless: true },
    );
  });

  it('omits --pretty when false', async () => {
    await harness.callTool('gog_people_raw', { userId: 'people/c123', pretty: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['people', 'raw', pos('people/c123')], { account: undefined, lossless: true });
  });
});

// SEC-3/SEC-4: every model-supplied server path must resolve inside an
// operator-configured root (GOG_FILE_ROOTS). The suite runs with '/' so the
// arg-shape tests can use any path; these narrow it.
async function withFileRoots<T>(roots: string, fn: () => Promise<T>): Promise<T> {
  const prev = process.env.GOG_FILE_ROOTS;
  process.env.GOG_FILE_ROOTS = roots;
  try {
    return await fn();
  } finally {
    process.env.GOG_FILE_ROOTS = prev;
  }
}

describe('server paths are confined to GOG_FILE_ROOTS', () => {
  it.each([
    ['gog_contacts_export', {"out": "/Users/me/.zshrc"}, 'out'],
  ] as Array<[string, Record<string, unknown>, string]>)('%s refuses %j outside the roots', async (tool, args, param) => {
    const h = harness;
    const result = await withFileRoots('/srv/gog-files', () => h.callTool(tool, args));
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toMatch(new RegExp(`${param} ".*" is outside the directories`));
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  // Clients auto-approve readOnlyHint tools; these write (and can overwrite)
  // files on the gog host, so they must not claim to be read-only.
  it.each(["gog_contacts_export"])('%s is not advertised as read-only and is marked destructive', async (name) => {
    const h = harness;
    const { tools } = await h.client.listTools();
    const tool = tools.find((t) => t.name === name)!;
    expect(tool.annotations?.readOnlyHint).not.toBe(true);
    expect(tool.annotations?.destructiveHint).toBe(true);
  });
});

describe('gog_contacts_export — stdout', () => {
  it('still accepts "-" (stdout) whatever the roots', async () => {
    await withFileRoots('/srv/gog-files', () => harness.callTool('gog_contacts_export', { out: '-' }));
    expect(lib.runOrDiagnose).toHaveBeenCalled();
  });
});
