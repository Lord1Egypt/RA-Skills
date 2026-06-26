#!/usr/bin/env node
import { runTransferSolCli } from '../src/cli/transfer-sol.js';

const code = await runTransferSolCli(process.argv, process.env);
process.exit(code);
