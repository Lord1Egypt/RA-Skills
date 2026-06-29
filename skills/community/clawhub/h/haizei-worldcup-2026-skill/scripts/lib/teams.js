#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, '..', '..', 'data', 'teams.json');

function loadTeams() {
  return JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
}

function listAllTeams(data) {
  const list = [];
  for (const [group, teams] of Object.entries(data.groups)) {
    for (const t of teams) {
      list.push({ group, position: t.position, teamName: t.teamName, teamId: t.teamId, pot: t.pot, isHost: !!t.isHost, qualifiedTop32: !!t.qualifiedTop32 });
    }
  }
  return list;
}

function findTeamByName(data, name) {
  for (const [group, teams] of Object.entries(data.groups)) {
    for (const t of teams) {
      if (t.teamName === name || t.teamName.includes(name)) {
        return { group, ...t };
      }
    }
  }
  return null;
}

function findTeamById(data, id) {
  for (const [group, teams] of Object.entries(data.groups)) {
    for (const t of teams) {
      if (t.teamId === id) return { group, ...t };
    }
  }
  return null;
}

function getGroup(data, groupKey) {
  const key = groupKey.toUpperCase();
  const teams = data.groups[key];
  return teams ? { group: key, teams } : null;
}

const HEX_ID_RE = /^[a-f0-9]{20,}$/;

function isTeamId(input) {
  return HEX_ID_RE.test(input);
}

function lookupTeam(input, data) {
  if (isTeamId(input)) return findTeamById(data, input);
  return findTeamByName(data, input);
}

function resolveTeamId(input, data) {
  const team = lookupTeam(input, data);
  return team ? team.teamId : null;
}

module.exports = { loadTeams, listAllTeams, findTeamByName, findTeamById, getGroup, lookupTeam, resolveTeamId, isTeamId };
