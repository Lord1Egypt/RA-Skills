/**
 * relays.js
 * List of public Nostr relays used for presence + discovery.
 * These are well-known, reliable public relays.
 */

const RELAYS = [
  'wss://relay.damus.io',
  'wss://relay.nostr.band',
  'wss://nos.lol',
  'wss://nostr.wine',
  'wss://relay.snort.social',
];

// Nostr event kind used for ocmesh presence announcements
// Kind 31337 is in the parameterized replaceable range — safe to use
const PRESENCE_KIND = 31337;

// Nostr kind for encrypted DMs (NIP-04)
const DM_KIND = 4;

// How often to re-announce presence (ms)
const ANNOUNCE_INTERVAL = 5 * 60 * 1000; // 5 minutes

// How often to scan for new peers (ms)
const DISCOVERY_INTERVAL = 2 * 60 * 1000; // 2 minutes

// Consider a peer "offline" if not seen in this window
const PEER_TTL = 15 * 60 * 1000; // 15 minutes

module.exports = {
  RELAYS,
  PRESENCE_KIND,
  DM_KIND,
  ANNOUNCE_INTERVAL,
  DISCOVERY_INTERVAL,
  PEER_TTL,
};
