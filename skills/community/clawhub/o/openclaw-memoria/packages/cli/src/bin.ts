#!/usr/bin/env node
/**
 * Binaire `memoria` — toutes les commandes sont enregistrées dans index.ts.
 */
import { buildCli } from './index.js'

await buildCli().runExit(process.argv.slice(2))
