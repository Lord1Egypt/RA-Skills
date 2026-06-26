'use strict';

const metadata = require('./metadata');

function inspectSkill() {
  return {
    name: metadata.name,
    version: metadata.version,
    status: 'ready-for-review'
  };
}

function summarizeSkill() {
  return `${metadata.name}@${metadata.version} is ready for publishing`;
}

module.exports = {
  inspectSkill,
  summarizeSkill
};
