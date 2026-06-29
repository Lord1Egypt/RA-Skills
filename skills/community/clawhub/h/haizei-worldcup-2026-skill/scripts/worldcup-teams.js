#!/usr/bin/env node

const { loadTeams, listAllTeams, findTeamByName, findTeamById, getGroup } = require('./lib/teams');

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const data = loadTeams();

  try {
    switch (command) {
      case 'list':
      case 'ls':
      case '--list': {
        console.log(JSON.stringify(listAllTeams(data), null, 2));
        break;
      }

      case 'group':
      case '-g': {
        const groupKey = args[1];
        if (!groupKey) {
          console.error('Error: 请提供小组标识，例如 A、B、C ... L');
          process.exit(1);
        }
        const groupData = getGroup(data, groupKey);
        if (!groupData) {
          console.error(`Error: 找不到 ${groupKey} 组`);
          process.exit(1);
        }
        console.log(JSON.stringify(groupData, null, 2));
        break;
      }

      case 'find':
      case '-f': {
        const keyword = args[1];
        if (!keyword) {
          console.error('Error: 请提供球队名称关键字');
          process.exit(1);
        }
        const team = findTeamByName(data, keyword);
        if (!team) {
          console.error(`Error: 找不到球队 ${keyword}`);
          process.exit(1);
        }
        console.log(JSON.stringify(team, null, 2));
        break;
      }

      case 'info': {
        console.log(JSON.stringify({
          tournament: data.tournament,
          tournamentEn: data.tournamentEn,
          season: data.season,
          hostCountries: data.hostCountries,
          totalTeams: data.totalTeams,
          totalGroups: data.totalGroups,
          teamsPerGroup: data.teamsPerGroup,
          matchUrl: data.matchUrl,
          rankingsUrl: data.rankingsUrl
        }, null, 2));
        break;
      }

      case 'hosts': {
        const hosts = listAllTeams(data).filter(t => t.isHost);
        console.log(JSON.stringify(hosts, null, 2));
        break;
      }

      case 'pot': {
        const pot = parseInt(args[1]);
        if (isNaN(pot) || pot < 1 || pot > 4) {
          console.error('Error: 档位必须在 1-4 之间');
          process.exit(1);
        }
        const teams = listAllTeams(data).filter(t => t.pot === pot);
        console.log(JSON.stringify({ pot, teams }, null, 2));
        break;
      }

      default:
        console.log(`
2026年世界杯球队配置查询工具

用法:
  node worldcup-teams.js <command> [options]

命令:
  list, ls, --list       列出所有48支球队
  group, -g <A-L>        查询指定小组的4支球队
  find, -f <球队名>      按名称模糊查找球队
  info                   查看赛事基本信息
  hosts                  列出东道主球队
  pot <1-4>              列出指定档位的球队

示例:
  node worldcup-teams.js list
  node worldcup-teams.js group A
  node worldcup-teams.js find 韩国
  node worldcup-teams.js info
  node worldcup-teams.js hosts
  node worldcup-teams.js pot 1
`);
        process.exit(0);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = { loadTeams, listAllTeams, findTeamByName, findTeamById, getGroup };

if (require.main === module) {
  main();
}
