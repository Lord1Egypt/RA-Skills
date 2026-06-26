/**
 * moltpost group <subcommand> [options]
 * create / add / broadcast / send / list / leave
 */

import crypto from 'crypto';
import {
  requireConfig,
  readGroups,
  writeGroups,
  appendAudit,
  updatePeersCache,
} from '../lib/storage.mjs';
import { createClient } from '../lib/broker.mjs';

function generateClientMsgId() {
  return `cmsg_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
}

export async function cmdGroup(args) {
  const subcommand = args[0];
  const subArgs = args.slice(1);

  switch (subcommand) {
    case 'create':
      return groupCreate(subArgs);
    case 'add':
      return groupAdd(subArgs);
    case 'leave':
      return groupLeave(subArgs);
    case 'list':
      return groupList(subArgs);
    case 'broadcast':
      return groupBroadcast(subArgs);
    case 'send':
      return groupSend(subArgs);
    default:
      console.error(`Unknown subcommand: ${subcommand}`);
      console.error('Available: create, add, leave, list, broadcast, send');
      process.exit(1);
  }
}

async function groupCreate(args) {
  const config = requireConfig();
  const groupId = args[0];

  if (!groupId) {
    console.error('Usage: moltpost group create <group_id> [--policy=owner_only|all_members|allowlist]');
    process.exit(1);
  }

  const policyArg = args.find((a) => a.startsWith('--policy='))?.slice(9) || 'owner_only';
  const client = createClient(config);

  const { status, data } = await client.groupCreate(groupId, config.clawid, [], {
    send_policy: policyArg,
  });

  if (status !== 200) {
    console.error(`Create group failed (${status}): ${data.error}`);
    process.exit(1);
  }

  const groups = readGroups();
  groups[groupId] = { owner: config.clawid, members: [config.clawid], cached_at: Date.now() };
  writeGroups(groups);

  appendAudit({ op: 'group_create', group_id: groupId });
  console.log(`✓ Group "${groupId}" created (policy: ${policyArg})`);
}

async function groupAdd(args) {
  const config = requireConfig();
  const groupId = args[0];
  const members = args.slice(1).filter((a) => !a.startsWith('--'));

  if (!groupId || members.length === 0) {
    console.error('Usage: moltpost group add <group_id> <clawid1> [clawid2 ...]');
    process.exit(1);
  }

  const client = createClient(config);

  const { status, data } = await client.groupPeers(groupId);
  if (status !== 200) {
    console.error(`Fetch group failed (${status}): ${data.error}`);
    process.exit(1);
  }

  console.log('Adding members requires the invite flow on the broker.');
  console.log(`Send an invite code to ${members.join(', ')}; they should run:`);
  console.log(`  moltpost group join ${groupId} --invite=<code>`);

  appendAudit({ op: 'group_add_intent', group_id: groupId, members });
}

async function groupLeave(args) {
  const config = requireConfig();
  const groupId = args[0];

  if (!groupId) {
    console.error('Usage: moltpost group leave <group_id> [--kick=<clawid>]');
    process.exit(1);
  }

  const kickClawid = args.find((a) => a.startsWith('--kick='))?.slice(7) || config.clawid;
  const client = createClient(config);

  const { status, data } = await client.groupLeave(groupId, kickClawid, config.clawid);

  if (status !== 200) {
    console.error(`Leave group failed (${status}): ${data.error}`);
    process.exit(1);
  }

  if (data.action === 'group_dissolved') {
    console.log(`✓ Group "${groupId}" dissolved (you were owner)`);
  } else {
    console.log(`✓ Left group "${groupId}"`);
  }

  appendAudit({ op: 'group_leave', group_id: groupId });
}

async function groupList(args) {
  requireConfig();
  const groups = readGroups();
  const groupIds = Object.keys(groups);

  if (groupIds.length === 0) {
    console.log('No cached groups.');
    return;
  }

  console.log(`\nCached groups (${groupIds.length}):\n`);
  for (const [id, info] of Object.entries(groups)) {
    console.log(`  ${id}  owner: ${info.owner || 'unknown'}  members: ${info.members?.length || '?'}`);
  }
  console.log('');
}

async function groupBroadcast(args) {
  const config = requireConfig();
  const groupId = args[0];
  const msgIdx = args.indexOf('--msg');
  const msg = msgIdx !== -1 ? args[msgIdx + 1] : args[1];

  if (!groupId || !msg) {
    console.error('Usage: moltpost group broadcast <group_id> --msg <text>');
    process.exit(1);
  }

  const client = createClient(config);
  const clientMsgId = generateClientMsgId();
  const ttlIdx = args.indexOf('--ttl');
  const ttlMinutes = ttlIdx !== -1 ? parseInt(args[ttlIdx + 1], 10) : null;
  const now = Math.floor(Date.now() / 1000);

  const { status, data } = await client.groupSend({
    group_id: groupId,
    from: config.clawid,
    mode: 'broadcast',
    data: msg,
    client_msg_id: clientMsgId,
    expires_at: ttlMinutes ? now + ttlMinutes * 60 : null,
  });

  if (status !== 200) {
    console.error(`Broadcast failed (${status}): ${data.error}`);
    appendAudit({ op: 'group_broadcast', group_id: groupId, status: 'error' });
    process.exit(1);
  }

  appendAudit({ op: 'group_broadcast', group_id: groupId, delivered_to: data.delivered_to, status: 'ok' });
  console.log(`✓ Broadcast delivered to ${data.delivered_to?.length || 0} member(s)`);
}

async function groupSend(args) {
  const config = requireConfig();
  const groupId = args[0];
  const toIdx = args.indexOf('--to');
  const msgIdx = args.indexOf('--msg');

  if (!groupId || toIdx === -1 || msgIdx === -1) {
    console.error('Usage: moltpost group send <group_id> --to <clawid> --msg <text>');
    process.exit(1);
  }

  const to = args[toIdx + 1];
  const msg = args[msgIdx + 1];
  const client = createClient(config);
  const clientMsgId = generateClientMsgId();
  const now = Math.floor(Date.now() / 1000);

  const { status, data } = await client.groupSend({
    group_id: groupId,
    from: config.clawid,
    mode: 'unicast',
    to: [to],
    data: msg,
    client_msg_id: clientMsgId,
  });

  if (status !== 200) {
    console.error(`Unicast failed (${status}): ${data.error}`);
    process.exit(1);
  }

  appendAudit({ op: 'group_unicast', group_id: groupId, to, status: 'ok' });
  console.log(`✓ Message sent to ${to}`);
}
