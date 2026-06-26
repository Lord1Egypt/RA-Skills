/**
 * prompt.js — TTY prompt helpers
 *
 * Readline-based helpers for interactive prompts.
 * Falls back gracefully when stdin is not a TTY.
 */

"use strict";

const readline = require("readline");

/**
 * Ask a yes/no question.
 * @param {string} question
 * @param {boolean} defaultYes — true → default Y, false → default N
 * @returns {boolean}
 */
function promptYesNo(question, defaultYes = false) {
  const prefix = defaultYes ? "[Y/n]" : "[y/N]";
  const answer = _prompt(`${question} ${prefix}: `);
  if (!answer) return defaultYes;
  return answer.toLowerCase() === "y";
}

/**
 * Ask for text input.
 * @param {string} question
 * @param {string} defaultValue
 * @returns {string}
 */
function promptText(question, defaultValue = "") {
  const suffix = defaultValue ? ` [${defaultValue}]` : "";
  const answer = _prompt(`${question}${suffix}: `);
  return answer || defaultValue;
}

/**
 * Show a menu and get user selection.
 * @param {string} promptText
 * @param {string[]} options
 * @param {number} defaultIndex
 * @returns {number} selected index
 */
function promptMenu(promptText, options, defaultIndex = 0) {
  console.log(promptText);
  options.forEach((opt, i) => {
    const marker = i === defaultIndex ? "*" : " ";
    console.log(`  [${i + 1}] ${marker} ${opt}`);
  });
  const answer = _prompt(`> `);
  if (!answer) return defaultIndex;
  const idx = parseInt(answer, 10) - 1;
  if (idx >= 0 && idx < options.length) return idx;
  return defaultIndex;
}

/**
 * @param {string} question
 * @returns {string}
 */
function _prompt(question) {
  if (!process.stdin.isTTY) return "";
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: true });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

// Sync versions for non-TTY contexts
function promptYesNoSync(question, defaultYes = false) {
  if (!process.stdin.isTTY) return false;
  return promptYesNo(question, defaultYes);
}

function promptTextSync(question, defaultValue = "") {
  if (!process.stdin.isTTY) return defaultValue;
  return promptText(question, defaultValue);
}

module.exports = {
  promptYesNo,
  promptText,
  promptMenu,
  promptYesNoSync,
  promptTextSync,
};
