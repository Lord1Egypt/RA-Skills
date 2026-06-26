import path from 'node:path';

export function buildScriptPaths(installDir) {
  const scriptsDir = path.join(installDir, 'scripts');
  return {
    scriptsDir,
    cli: path.join(scriptsDir, 'insentek_cli.py'),
    exportExcel: path.join(scriptsDir, 'export_excel.py'),
    writeHtml: path.join(scriptsDir, 'write_html.py'),
  };
}
