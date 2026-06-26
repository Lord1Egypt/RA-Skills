#!/usr/bin/env node

let Command;
let chalk;
let ora;

try {
  ({ Command } = require('commander'));
  chalk = require('chalk');
  ora = require('ora');
} catch (error) {
  const KnowledgeConnector = require('../src/index.js');
  const kc = new KnowledgeConnector();

  if (process.argv[2] === 'doctor') {
    const report = kc.doctor();
    console.log('\nKnowledge Connector Doctor');
    console.log(`  Version: ${report.version || 'unknown'}`);
    console.log(`  Data dir: ${report.dataDir}`);
    console.log(`  Package root: ${report.packageRoot}`);
    console.log('\nChecks:');
    report.checks.forEach((check) => {
      const marker = check.ok ? 'OK' : (check.severity === 'warning' ? 'WARN' : 'FAIL');
      console.log(`  [${marker}] ${check.name}: ${check.detail}`);
    });
    process.exit(report.ok ? 0 : 1);
  }

  console.error(`Knowledge Connector CLI dependencies are missing: ${error.message}`);
  console.error('Run `npm install` in the package directory or reinstall with `clawhub install knowledge-connector`.');
  console.error('You can still run `node bin/cli.js doctor` for installation diagnostics.');
  process.exit(1);
}

const KnowledgeConnector = require('../src/index.js');

const program = new Command();
const kc = new KnowledgeConnector();

program
  .name('knowledge-connector')
  .description('Knowledge Connector - 导入向导、跨文档答案页、可视化关系、输出可操作知识图谱结果')
  .version('1.3.0');

// 提取命令
program
  .command('extract')
  .description('从文本或单个文件中提取概念')
  .option('-f, --file <path>', '从文件提取')
  .option('-t, --text <text>', '从文本提取')
  .option('-s, --save', '保存到知识库')
  .option('-o, --output <path>', '输出到文件')
  .action(async (options) => {
    const spinner = ora('正在提取概念...').start();
    
    try {
      let content = '';
      
      if (options.file) {
        const fs = require('fs');
        content = fs.readFileSync(options.file, 'utf-8');
      } else if (options.text) {
        content = options.text;
      } else {
        spinner.fail('请提供 -f 或 -t 参数');
        process.exit(1);
      }
      
      const concepts = await kc.extract(content);
      spinner.succeed(`成功提取 ${concepts.length} 个概念`);
      
      if (options.save) {
        await kc.saveConcepts(concepts);
        console.log(chalk.green('✓ 概念已保存到知识库'));
      }
      
      if (options.output) {
        const fs = require('fs');
        fs.writeFileSync(options.output, JSON.stringify(concepts, null, 2));
        console.log(chalk.green(`✓ 结果已保存到 ${options.output}`));
      }
      
      // 显示提取的概念
      console.log(chalk.blue('\n提取的概念:'));
      concepts.forEach((c, i) => {
        console.log(`  ${i + 1}. ${chalk.bold(c.name)} ${chalk.gray(`(${c.type})`)}`);
        if (c.description) {
          console.log(`     ${c.description}`);
        }
      });
    } catch (error) {
      spinner.fail(`提取失败: ${error.message}`);
      process.exit(1);
    }
  });

program
  .command('import-docs')
  .description('批量导入文档或目录，并自动建立跨文档关系')
  .option('-f, --files <paths...>', '导入多个文件')
  .option('-d, --dir <path>', '导入整个目录')
  .option('--no-auto-connect', '导入后不自动关联')
  .action(async (options) => {
    const spinner = ora('正在导入文档...').start();
    try {
      const inputs = options.files && options.files.length > 0 ? options.files : (options.dir ? [options.dir] : []);
      if (inputs.length === 0) {
        spinner.fail('请提供 --files 或 --dir 参数');
        process.exit(1);
      }

      const summary = await kc.importDocuments(inputs, { autoConnect: options.autoConnect });
      spinner.succeed(`成功导入 ${summary.fileCount} 个来源文档`);
      console.log(chalk.blue('\n导入结果:'));
      console.log(`  文档数量: ${chalk.bold(summary.fileCount)}`);
      console.log(`  新增来源: ${chalk.bold(summary.newSourceCount)}`);
      console.log(`  更新来源: ${chalk.bold(summary.updatedSourceCount)}`);
      console.log(`  概念数量: ${chalk.bold(summary.conceptCount)}`);
      console.log(`  新关系数量: ${chalk.bold(summary.relationCount)}`);
      if (summary.files.length > 0) {
        console.log(chalk.blue('\n已导入来源:'));
        summary.files.slice(0, 10).forEach((file, index) => {
          console.log(`  ${index + 1}. ${chalk.bold(file.title)} ${chalk.gray(`(${file.conceptCount} concepts)`)}`);
        });
      }
    } catch (error) {
      spinner.fail(`导入失败: ${error.message}`);
      process.exit(1);
    }
  });

program
  .command('import-wizard')
  .description('预览导入范围，再一步执行导入')
  .option('-f, --files <paths...>', '预览多个文件')
  .option('-d, --dir <path>', '预览整个目录')
  .option('--run', '预览后立即执行导入')
  .option('--no-auto-connect', '导入后不自动关联')
  .action(async (options) => {
    const spinner = ora('正在分析导入范围...').start();
    try {
      const inputs = options.files && options.files.length > 0 ? options.files : (options.dir ? [options.dir] : []);
      if (inputs.length === 0) {
        spinner.fail('请提供 --files 或 --dir 参数');
        process.exit(1);
      }

      const plan = kc.planImport(inputs);
      spinner.succeed(`预计可导入 ${plan.fileCount} 个文件`);
      console.log(chalk.blue('\n导入预览:'));
      console.log(`  文件数量: ${chalk.bold(plan.fileCount)}`);
      console.log(`  支持类型: ${chalk.bold(plan.supportedTypes.join(', ') || '无')}`);
      plan.files.slice(0, 12).forEach((file, index) => {
        console.log(`  ${index + 1}. ${chalk.bold(file.title)} ${chalk.gray(file.path)}`);
      });

      if (!options.run) {
        console.log(chalk.yellow('\n这是预览模式。加上 --run 会直接执行导入。'));
        return;
      }

      const summary = await kc.importDocuments(inputs, { autoConnect: options.autoConnect });
      console.log(chalk.green('\n✓ 导入完成'));
      console.log(`  文档数量: ${chalk.bold(summary.fileCount)}`);
      console.log(`  新增来源: ${chalk.bold(summary.newSourceCount)}`);
      console.log(`  更新来源: ${chalk.bold(summary.updatedSourceCount)}`);
      console.log(`  概念数量: ${chalk.bold(summary.conceptCount)}`);
      console.log(`  新关系数量: ${chalk.bold(summary.relationCount)}`);
    } catch (error) {
      spinner.fail(`导入向导失败: ${error.message}`);
      process.exit(1);
    }
  });

// 关联命令
program
  .command('connect')
  .description('建立概念间的关联')
  .option('-a, --auto', '自动分析并建立关联')
  .option('--from <concept>', '源概念')
  .option('--to <concept>', '目标概念')
  .option('--relation <type>', '关系类型', '相关')
  .option('--file <path>', '从文件批量导入关系')
  .action(async (options) => {
    const spinner = ora('正在建立关联...').start();
    
    try {
      if (options.auto) {
        const relations = await kc.autoConnect();
        spinner.succeed(`自动建立了 ${relations.length} 个关联`);
      } else if (options.from && options.to) {
        const relation = await kc.connect({
          from: options.from,
          to: options.to,
          type: options.relation
        });
        spinner.succeed(`已建立关联: ${options.from} → ${options.relation} → ${options.to}`);
      } else if (options.file) {
        const fs = require('fs');
        const data = JSON.parse(fs.readFileSync(options.file, 'utf-8'));
        const relations = await kc.importRelations(data);
        spinner.succeed(`从文件导入了 ${relations.length} 个关联`);
      } else {
        spinner.fail('请提供 --auto、--from/--to 或 --file 参数');
        process.exit(1);
      }
    } catch (error) {
      spinner.fail(`建立关联失败: ${error.message}`);
      process.exit(1);
    }
  });

// 查询命令
program
  .command('query')
  .description('查询知识库并返回跨文档结果')
  .argument('[keyword]', '搜索关键词')
  .option('-c, --concept <name>', '查询特定概念')
  .option('-d, --detail', '显示详细信息')
  .option('-r, --related', '显示关联概念')
  .option('-t, --type <type>', '按类型筛选')
  .option('-a, --ask <question>', '自然语言查询')
  .option('-s, --sources', '显示命中的来源文档')
  .action(async (keyword, options) => {
    const spinner = ora('正在查询...').start();
    
    try {
      let results = [];
      
      if (options.ask) {
        results = await kc.ask(options.ask);
        spinner.succeed('查询完成');
        console.log(chalk.blue('\n答案:'));
        console.log(results.answer || '未找到答案');
        if (results.nextSteps && results.nextSteps.length > 0) {
          console.log(chalk.blue('\n下一步建议:'));
          results.nextSteps.forEach((step) => console.log(`  • ${step}`));
        }
        return;
      }
      
      if (options.concept) {
        const concept = await kc.getConcept(options.concept);
        spinner.succeed('查询完成');
        
        if (!concept) {
          console.log(chalk.yellow(`未找到概念: ${options.concept}`));
          return;
        }
        
        console.log(chalk.blue('\n概念详情:'));
        console.log(`  名称: ${chalk.bold(concept.name)}`);
        console.log(`  类型: ${concept.type}`);
        console.log(`  描述: ${concept.description || '无'}`);
        console.log(`  别名: ${(concept.aliases || []).join(', ') || '无'}`);
        
        if (options.related) {
          const related = await kc.getRelated(concept.id);
          console.log(chalk.blue('\n关联概念:'));
          related.forEach(r => {
            console.log(`  • ${r.name} ${chalk.gray(`(${r.relationType})`)}`);
          });
        }
      } else if (keyword) {
        results = await kc.search(keyword);
        spinner.succeed(`找到 ${results.concepts.length} 个概念结果`);
        
        console.log(chalk.blue('\n搜索结果:'));
        results.concepts.forEach((r, i) => {
          console.log(`  ${i + 1}. ${chalk.bold(r.name)} ${chalk.gray(`(${r.type})`)}`);
          if (options.detail && r.description) {
            console.log(`     ${r.description}`);
          }
        });

        if (options.sources && results.sources.length > 0) {
          console.log(chalk.blue('\n命中的来源文档:'));
          results.sources.slice(0, 10).forEach((source, i) => {
            console.log(`  ${i + 1}. ${chalk.bold(source.title)} ${chalk.gray(source.path)}`);
          });
        }

        if (results.nextSteps.length > 0) {
          console.log(chalk.blue('\n下一步建议:'));
          results.nextSteps.forEach((step) => console.log(`  • ${step}`));
        }
      } else {
        spinner.fail('请提供搜索关键词或 --concept 参数');
        process.exit(1);
      }
    } catch (error) {
      spinner.fail(`查询失败: ${error.message}`);
      process.exit(1);
    }
  });

program
  .command('search')
  .description('做跨文档搜索，返回概念、来源文档和下一步动作')
  .argument('<keyword>', '搜索关键词')
  .action(async (keyword) => {
    const spinner = ora('正在跨文档搜索...').start();
    try {
      const result = await kc.search(keyword);
      spinner.succeed(`搜索完成，命中 ${result.concepts.length} 个概念和 ${result.sources.length} 个来源`);
      console.log(chalk.blue('\n概念结果:'));
      result.concepts.slice(0, 10).forEach((concept, index) => {
        console.log(`  ${index + 1}. ${chalk.bold(concept.name)} ${chalk.gray(`(${concept.type})`)}`);
      });
      if (result.sources.length > 0) {
        console.log(chalk.blue('\n来源文档:'));
        result.sources.slice(0, 10).forEach((source, index) => {
          console.log(`  ${index + 1}. ${chalk.bold(source.title)} ${chalk.gray(source.path)}`);
        });
      }
      if (result.nextSteps.length > 0) {
        console.log(chalk.blue('\n下一步建议:'));
        result.nextSteps.forEach((step) => console.log(`  • ${step}`));
      }
    } catch (error) {
      spinner.fail(`搜索失败: ${error.message}`);
      process.exit(1);
    }
  });

program
  .command('answer')
  .description('把跨文档搜索整理成更像答案页的结果')
  .argument('<query>', '问题或查询')
  .option('-f, --format <format>', '输出格式 (json/html)', 'json')
  .option('-o, --output <path>', '输出文件路径')
  .action(async (query, options) => {
    const spinner = ora('正在生成答案页...').start();
    try {
      const result = await kc.answer(query, { format: options.format });
      spinner.succeed('答案生成完成');

      if (options.output) {
        const fs = require('fs');
        const payload = typeof result === 'string' ? result : JSON.stringify(result, null, 2);
        fs.writeFileSync(options.output, payload);
        console.log(chalk.green(`✓ 结果已保存到 ${options.output}`));
        return;
      }

      if (typeof result === 'string') {
        console.log(result);
        return;
      }

      console.log(chalk.blue('\n答案摘要:'));
      console.log(result.summary);
      if (result.nextSteps.length > 0) {
        console.log(chalk.blue('\n下一步建议:'));
        result.nextSteps.forEach((step) => console.log(`  • ${step}`));
      }
    } catch (error) {
      spinner.fail(`答案生成失败: ${error.message}`);
      process.exit(1);
    }
  });

program
  .command('map')
  .description('围绕一个概念生成可操作的子图结果')
  .requiredOption('-c, --concept <name>', '中心概念')
  .option('-d, --depth <n>', '关联深度', '2')
  .option('-o, --output <path>', '输出 JSON 文件')
  .action(async (options) => {
    const spinner = ora('正在生成子图...').start();
    try {
      const result = await kc.map(options.concept, parseInt(options.depth, 10));
      if (!result) {
        spinner.fail(`未找到概念: ${options.concept}`);
        process.exit(1);
      }
      spinner.succeed(`已生成 ${result.nodes.length} 个概念、${result.edges.length} 条关系的子图`);
      if (options.output) {
        const fs = require('fs');
        fs.writeFileSync(options.output, JSON.stringify(result, null, 2));
        console.log(chalk.green(`✓ 子图已保存到 ${options.output}`));
      }
      console.log(chalk.blue('\n中心概念:'));
      console.log(`  ${chalk.bold(result.center.name)}`);
      console.log(chalk.blue('\n下一步建议:'));
      result.nextSteps.forEach((step) => console.log(`  • ${step}`));
    } catch (error) {
      spinner.fail(`生成子图失败: ${error.message}`);
      process.exit(1);
    }
  });

// 可视化命令
program
  .command('visualize')
  .description('生成知识图谱可视化')
  .option('-f, --format <format>', '输出格式 (html/json/dot)', 'html')
  .option('-o, --output <path>', '输出文件路径')
  .option('-c, --concept <name>', '以特定概念为中心')
  .option('-d, --depth <n>', '关联深度', '2')
  .action(async (options) => {
    const spinner = ora('正在生成可视化...').start();
    
    try {
      const result = await kc.visualize({
        format: options.format,
        concept: options.concept,
        depth: parseInt(options.depth)
      });
      
      if (options.output) {
        const fs = require('fs');
        fs.writeFileSync(options.output, result);
        spinner.succeed(`可视化已保存到 ${options.output}`);
      } else {
        spinner.succeed('可视化生成完成');
        console.log(result);
      }
    } catch (error) {
      spinner.fail(`可视化失败: ${error.message}`);
      process.exit(1);
    }
  });

// 统计命令
program
  .command('stats')
  .description('显示知识库统计信息')
  .action(async () => {
    const spinner = ora('正在统计...').start();
    
    try {
      const stats = await kc.getStats();
      spinner.succeed('统计完成');
      
      console.log(chalk.blue('\n知识库统计:'));
      console.log(`  概念数量: ${chalk.bold(stats.conceptCount)}`);
      console.log(`  关系数量: ${chalk.bold(stats.relationCount)}`);
      console.log(`  来源文档: ${chalk.bold(stats.sourceCount)}`);
      console.log(`  概念类型: ${chalk.bold(stats.typeCount)} 种`);
      console.log(`  数据大小: ${chalk.bold(stats.dataSize)}`);
    } catch (error) {
      spinner.fail(`统计失败: ${error.message}`);
      process.exit(1);
    }
  });

program
  .command('doctor')
  .description('检查安装、数据目录、JSON 数据和 kc 命令可用性')
  .action(() => {
    const report = kc.doctor();
    console.log(chalk.blue('\nKnowledge Connector Doctor'));
    console.log(`  版本: ${chalk.bold(report.version || 'unknown')}`);
    console.log(`  数据目录: ${report.dataDir}`);
    console.log(`  包目录: ${report.packageRoot}`);
    console.log(chalk.blue('\n检查项:'));
    report.checks.forEach((check) => {
      const marker = check.ok ? chalk.green('✓') : (check.severity === 'warning' ? chalk.yellow('!') : chalk.red('x'));
      console.log(`  ${marker} ${check.name}: ${check.detail}`);
    });
    if (!report.ok) {
      process.exit(1);
    }
  });

// 导出命令
program
  .command('export')
  .description('导出知识库')
  .option('-o, --output <path>', '输出文件路径', 'knowledge-export.json')
  .action(async (options) => {
    const spinner = ora('正在导出...').start();
    
    try {
      const data = await kc.export();
      const fs = require('fs');
      fs.writeFileSync(options.output, JSON.stringify(data, null, 2));
      spinner.succeed(`知识库已导出到 ${options.output}`);
    } catch (error) {
      spinner.fail(`导出失败: ${error.message}`);
      process.exit(1);
    }
  });

// 导入命令
program
  .command('import')
  .description('导入知识库')
  .option('-f, --file <path>', '导入文件路径')
  .action(async (options) => {
    if (!options.file) {
      console.error(chalk.red('请提供 --file 参数'));
      process.exit(1);
    }
    
    const spinner = ora('正在导入...').start();
    
    try {
      const fs = require('fs');
      const data = JSON.parse(fs.readFileSync(options.file, 'utf-8'));
      await kc.import(data);
      spinner.succeed('知识库导入完成');
    } catch (error) {
      spinner.fail(`导入失败: ${error.message}`);
      process.exit(1);
    }
  });

// 清空命令
program
  .command('clear')
  .description('清空知识库')
  .option('--confirm', '确认清空')
  .action(async (options) => {
    if (!options.confirm) {
      console.log(chalk.yellow('警告: 此操作将清空所有数据！'));
      console.log(chalk.gray('请使用 --confirm 参数确认'));
      process.exit(0);
    }
    
    const spinner = ora('正在清空...').start();
    
    try {
      await kc.clear();
      spinner.succeed('知识库已清空');
    } catch (error) {
      spinner.fail(`清空失败: ${error.message}`);
      process.exit(1);
    }
  });

// 推荐命令
program
  .command('recommend')
  .description('推荐相关知识')
  .argument('<concept>', '概念名称')
  .option('-n, --limit <n>', '推荐数量', '5')
  .action(async (concept, options) => {
    const spinner = ora('正在生成推荐...').start();
    
    try {
      const recommendations = await kc.recommend(concept, parseInt(options.limit));
      spinner.succeed('推荐生成完成');
      
      console.log(chalk.blue(`\n与 "${concept}" 相关的知识:`));
      recommendations.forEach((r, i) => {
        console.log(`  ${i + 1}. ${chalk.bold(r.name)} ${chalk.gray(`(相关度: ${r.score.toFixed(2)})`)}`);
        if (r.reason) {
          console.log(`     ${r.reason}`);
        }
      });
    } catch (error) {
      spinner.fail(`推荐失败: ${error.message}`);
      process.exit(1);
    }
  });

program.parse();
