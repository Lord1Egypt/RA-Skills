#!/usr/bin/env node
const { generateSecretKey, getPublicKey, finalizeEvent } = require('nostr-tools/pure');
const { Relay } = require('nostr-tools/relay');
const { bytesToHex, hexToBytes } = require('@noble/hashes/utils');
const fs = require('fs');
const path = require('path');

// Dynamic Config - Uses OpenClaw defaults or fallbacks
const AGENT_NAME = process.env.OPENCLAW_AGENT_NAME || "DogeBot";
const CONFIG_DIR = path.join(process.env.HOME, '.openclaw', 'nostr-dogechat');
const IDENTITY_FILE = path.join(CONFIG_DIR, 'identity.json');
const RELAYS = ['wss://relay.damus.io', 'wss://nos.lol', 'wss://relay.dogechat.org'];

function getIdentity() {
    if (!fs.existsSync(CONFIG_DIR)) fs.mkdirSync(CONFIG_DIR, { recursive: true });
    let identity = null;
    if (fs.existsSync(IDENTITY_FILE)) {
        const stats = fs.statSync(IDENTITY_FILE);
        const ageHours = (new Date() - stats.mtime) / (1000 * 60 * 60);
        if (ageHours < 24) identity = JSON.parse(fs.readFileSync(IDENTITY_FILE));
    }
    if (!identity) {
        const sk = generateSecretKey();
        const nsec = bytesToHex(sk);
        identity = { nsec, createdAt: new Date().toISOString() };
        fs.writeFileSync(IDENTITY_FILE, JSON.stringify(identity));
    }
    return identity;
}

async function sendMessage(geohash, message) {
    const { nsec } = getIdentity();
    const sk = hexToBytes(nsec);
    const event = finalizeEvent({
        kind: 1,
        created_at: Math.floor(Date.now() / 1000),
        tags: [['g', geohash], ['t', 'd0ge'], ['agent', AGENT_NAME]],
        content: `[${AGENT_NAME}]: ${message}`,
    }, sk);

    for (const url of RELAYS) {
        try {
            const relay = await Relay.connect(url);
            await relay.publish(event);
            relay.close();
        } catch (e) {}
    }
}

// CLI Parsing
const args = require('minimist')(process.argv.slice(2));
if (args._[0] === 'send') {
    const hash = args.geohash || 'd0ge'; // Default to global if no geohash
    const msg = args.message || args._.slice(1).join(' ');
    sendMessage(hash, msg);
}