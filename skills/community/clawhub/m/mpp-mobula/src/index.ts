#!/usr/bin/env bun

/**
 * MPP (Machine Payments Protocol) CLI
 * Manage Mobula API subscriptions and fetch market data
 */

import { mppCommand } from "./commands/mpp";

const args = process.argv.slice(2);

if (args.length === 0) {
  mppCommand(["help"]);
} else {
  mppCommand(args);
}
