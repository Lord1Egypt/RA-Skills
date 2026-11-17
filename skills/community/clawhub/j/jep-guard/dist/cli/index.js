#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const commander_1 = require("commander");
const init_1 = require("./commands/init");
const daemon_1 = require("./commands/daemon");
const skills_1 = require("./commands/skills");
const judge_1 = require("./commands/judge");
const delegate_1 = require("./commands/delegate");
const verify_1 = require("./commands/verify");
const terminate_1 = require("./commands/terminate");
const export_1 = require("./commands/export");
const status_1 = require("./commands/status");
const dashboard_1 = require("./commands/dashboard");
const program = new commander_1.Command();
program
    .name('jep-guard')
    .description('JEP Guard v3.0.0 — Causal Operating System for OpenClaw Skills')
    .version('2.0.4');
program.addCommand(init_1.initCommand);
program.addCommand(daemon_1.daemonCommand);
program.addCommand(skills_1.skillsCommand);
program.addCommand(judge_1.judgeCommand);
program.addCommand(delegate_1.delegateCommand);
program.addCommand(verify_1.verifyCommand);
program.addCommand(terminate_1.terminateCommand);
program.addCommand(export_1.exportCommand);
program.addCommand(status_1.statusCommand);
program.addCommand(dashboard_1.dashboardCommand);
program.parse();
//# sourceMappingURL=index.js.map