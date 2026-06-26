#!/usr/bin/env node

import { main } from "./src/reminders.js";

const exitCode = await main(process.argv.slice(2));
process.exit(exitCode);
