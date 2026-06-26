#!/usr/bin/env node

/**
 * invoice-scan CLI
 * 
 * Usage:
 *   invoice-scan scan <file> [--provider claude] [--format json|csv|excel] [--output result.json]
 *   invoice-scan providers
 *   invoice-scan formats
 *   invoice-scan version
 */

const fs = require('fs');
const path = require('path');
const { scanInvoice } = require('./extraction/scanner');
const { formatOutput, listFormats } = require('./output/index');
const { listProviders } = require('./adapters/index');
const pkg = require('./package.json');

const args = process.argv.slice(2);
const command = args[0];

function getArg(name, fallback = null) {
  const idx = args.indexOf(`--${name}`);
  if (idx === -1 || idx + 1 >= args.length) return fallback;
  return args[idx + 1];
}

function hasFlag(name) {
  return args.includes(`--${name}`);
}

async function main() {
  switch (command) {
    case 'scan': {
      const filePath = args[1];
      if (!filePath) {
        console.error('Usage: invoice-scan scan <file> [--provider claude] [--format json] [--output result.json]');
        process.exit(1);
      }

      const provider = getArg('provider', 'claude');
      const format = getArg('format', 'json');
      const outputPath = getArg('output');
      const model = getArg('model');
      const noPreprocess = hasFlag('no-preprocess');
      const acceptTypes = getArg('accept', 'relaxed'); // strict, relaxed, any

      // Get API key from args or env
      let apiKey = getArg('api-key');
      if (!apiKey) {
        const envMap = {
          claude: 'ANTHROPIC_API_KEY',
          openai: 'OPENAI_API_KEY',
          gemini: 'GOOGLE_API_KEY',
        };
        apiKey = process.env[envMap[provider] || 'ANTHROPIC_API_KEY'];
      }

      if (!apiKey) {
        console.error(`No API key found. Set --api-key or ${provider === 'claude' ? 'ANTHROPIC_API_KEY' : 'appropriate'} env var.`);
        process.exit(1);
      }

      console.log(`🦇 Scanning: ${filePath}`);
      console.log(`   Provider: ${provider}`);
      console.log(`   Format: ${format}`);
      console.log('');

      try {
        const invoice = await scanInvoice(path.resolve(filePath), {
          provider,
          apiKey,
          model,
          preprocess: !noPreprocess,
          acceptTypes,
        });

        const output = formatOutput(invoice, format);

        if (outputPath) {
          const ext = format === 'excel' || format === 'xlsx' ? '.xlsx' : `.${format}`;
          const outFile = outputPath.includes('.') ? outputPath : outputPath + ext;

          if (Buffer.isBuffer(output)) {
            fs.writeFileSync(outFile, output);
          } else {
            fs.writeFileSync(outFile, output, 'utf8');
          }
          console.log(`✅ Output saved to: ${outFile}`);
        } else {
          if (Buffer.isBuffer(output)) {
            console.log('(Excel output requires --output <file>)');
          } else {
            console.log(output);
          }
        }

        // Summary
        console.log('');
        console.log(`📊 Status: ${invoice.exceptions.overallStatus}`);
        console.log(`   Confidence: ${invoice.metadata.confidence}`);
        console.log(`   Line items: ${invoice.lineItems.length}`);
        console.log(`   Arithmetic: ${invoice.validation.arithmeticValid ? '✅' : '❌'}`);
        if (invoice.validation.errors.length > 0) {
          console.log(`   Errors: ${invoice.validation.errors.length}`);
          for (const err of invoice.validation.errors) {
            console.log(`     - ${err.field}: ${err.message}`);
          }
        }
        if (invoice.metadata.documentType) {
          console.log(`   Doc type: ${invoice.metadata.documentType}`);
        }
        if (invoice.validation.documentQuality) {
          const q = invoice.validation.documentQuality;
          console.log(`   Quality: ${q.rating} (${q.score} — ${q.presentFields}/${q.totalChecked} key fields)`);
        }
        if (invoice.validation.warnings.length > 0) {
          console.log(`   Warnings: ${invoice.validation.warnings.length}`);
        }
        console.log(`   Duration: ${invoice.metadata.processingDurationMs}ms`);
      } catch (err) {
        console.error(`❌ Error: ${err.message}`);
        process.exit(1);
      }
      break;
    }

    case 'providers':
      console.log('Available providers:');
      for (const p of listProviders()) {
        console.log(`  - ${p}`);
      }
      break;

    case 'formats':
      console.log('Available output formats:');
      for (const f of listFormats()) {
        console.log(`  - ${f}`);
      }
      break;

    case 'version':
      console.log(`invoice-scan v${pkg.version}`);
      break;

    default:
      console.log(`🦇 invoice-scan v${pkg.version}`);
      console.log('');
      console.log('Usage:');
      console.log('  invoice-scan scan <file> [options]    Scan an invoice');
      console.log('  invoice-scan providers                List AI providers');
      console.log('  invoice-scan formats                  List output formats');
      console.log('  invoice-scan version                  Show version');
      console.log('');
      console.log('Options:');
      console.log('  --provider <name>     AI provider (default: claude)');
      console.log('  --format <format>     Output format: json, csv, excel');
      console.log('  --output <file>       Save output to file');
      console.log('  --api-key <key>       API key (or use env var)');
      console.log('  --model <name>        Model override');
      console.log('  --no-preprocess       Skip image pre-processing');
  }
}

main().catch(err => {
  console.error(`Fatal: ${err.message}`);
  process.exit(1);
});
