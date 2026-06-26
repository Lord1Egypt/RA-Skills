#!/usr/bin/env node
/**
 * Seed a MusicBrainz release from a JSON definition.
 * 
 * Usage: node seed_release.mjs <release.json>
 * 
 * Outputs: multipart/form-data body suitable for POST to /release/add
 * In practice: generates an HTML file that auto-submits the form,
 * which can be opened in the browser to land on a pre-filled release editor.
 * 
 * JSON schema:
 * {
 *   "name": "Endstation",
 *   "artist": { "mbid": "78e8899b-...", "name": "kevin" },
 *   "type": "Album",           // Album, EP, Single, Broadcast, Other
 *   "status": "official",      // official, promotion, bootleg, pseudo-release
 *   "language": "deu",         // ISO 639-3
 *   "script": "Latn",          // ISO 15924
 *   "packaging": "None",
 *   "barcode": "none",         // "none" = no barcode, or actual barcode string
 *   "events": [{ "year": 2023, "month": 4, "day": 28, "country": "XW" }],
 *   "labels": [{ "name": "Vertigo Berlin", "mbid": "bb7f25ac-...", "catalog": "" }],
 *   "tracks": [
 *     { "name": "Erbgut", "length": "0:54" },
 *     { "name": "Filter", "length": "2:24" }
 *   ],
 *   "urls": [{ "url": "https://open.spotify.com/album/...", "link_type": 85 }],
 *   "edit_note": "Added from Spotify"
 * }
 */

import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';

const jsonPath = process.argv[2];
if (!jsonPath) {
  console.error('Usage: node seed_release.mjs <release.json>');
  process.exit(1);
}

const release = JSON.parse(readFileSync(jsonPath, 'utf-8'));

// Build form fields
const fields = [];
function add(name, value) {
  if (value !== undefined && value !== null && value !== '') {
    fields.push({ name, value: String(value) });
  }
}

// Release info
add('name', release.name);
if (release.type) add('type', release.type);
if (release.release_group) add('release_group', release.release_group);
if (release.comment) add('comment', release.comment);
if (release.annotation) add('annotation', release.annotation);
if (release.status) add('status', release.status);
if (release.language) add('language', release.language);
if (release.script) add('script', release.script);
if (release.packaging) add('packaging', release.packaging);
if (release.barcode !== undefined) add('barcode', release.barcode);

// Artist credit
if (release.artist) {
  const a = release.artist;
  if (a.mbid) add('artist_credit.names.0.mbid', a.mbid);
  if (a.name) add('artist_credit.names.0.artist.name', a.name);
  if (a.credited_name) add('artist_credit.names.0.name', a.credited_name);
}
if (release.artists) {
  release.artists.forEach((a, i) => {
    if (a.mbid) add(`artist_credit.names.${i}.mbid`, a.mbid);
    if (a.name) add(`artist_credit.names.${i}.artist.name`, a.name);
    if (a.credited_name) add(`artist_credit.names.${i}.name`, a.credited_name);
    if (a.join_phrase) add(`artist_credit.names.${i}.join_phrase`, a.join_phrase);
  });
}

// Events
if (release.events) {
  release.events.forEach((e, i) => {
    if (e.year) add(`events.${i}.date.year`, e.year);
    if (e.month) add(`events.${i}.date.month`, e.month);
    if (e.day) add(`events.${i}.date.day`, e.day);
    if (e.country) add(`events.${i}.country`, e.country);
  });
}

// Labels
if (release.labels) {
  release.labels.forEach((l, i) => {
    if (l.mbid) add(`labels.${i}.mbid`, l.mbid);
    if (l.name) add(`labels.${i}.name`, l.name);
    if (l.catalog !== undefined) add(`labels.${i}.catalog_number`, l.catalog);
  });
}

// Mediums / tracks
const tracks = release.tracks || [];
add('mediums.0.format', release.medium_format || 'Digital Media');
if (release.medium_name) add('mediums.0.name', release.medium_name);
tracks.forEach((t, i) => {
  add(`mediums.0.track.${i}.name`, t.name);
  if (t.length) add(`mediums.0.track.${i}.length`, t.length);
  if (t.number) add(`mediums.0.track.${i}.number`, t.number);
  if (t.recording) add(`mediums.0.track.${i}.recording`, t.recording);
  // Track artist credit (if different from release artist)
  if (t.artist) {
    if (t.artist.mbid) add(`mediums.0.track.${i}.artist_credit.names.0.mbid`, t.artist.mbid);
    if (t.artist.name) add(`mediums.0.track.${i}.artist_credit.names.0.artist.name`, t.artist.name);
  }
});

// URLs
if (release.urls) {
  release.urls.forEach((u, i) => {
    add(`urls.${i}.url`, u.url);
    if (u.link_type) add(`urls.${i}.link_type`, u.link_type);
  });
}

// Edit note
if (release.edit_note) add('edit_note', release.edit_note);

// Generate self-submitting HTML form
const htmlFields = fields.map(f => 
  `  <input type="hidden" name="${f.name.replace(/"/g, '&quot;')}" value="${f.value.replace(/"/g, '&quot;')}">`
).join('\n');

const html = `<!DOCTYPE html>
<html>
<head><title>Seeding MusicBrainz Release</title></head>
<body>
<p>Submitting to MusicBrainz release editor...</p>
<form id="seed" method="post" action="https://musicbrainz.org/release/add">
${htmlFields}
</form>
<script>document.getElementById('seed').submit();</script>
</body>
</html>`;

const outPath = resolve('/tmp/openclaw/uploads/seed-release.html');
writeFileSync(outPath, html);
console.log(`Seed form written to: ${outPath}`);
console.log(`Fields: ${fields.length}`);
console.log('\nTo use: open this file in the MB-authenticated browser session.');

// Also output fields as summary
console.log('\n--- Seeded fields ---');
fields.forEach(f => console.log(`  ${f.name} = ${f.value}`));
