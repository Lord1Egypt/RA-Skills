function pad(str: string, len: number) {
  return str + ' '.repeat(len - str.length)
}

export function printPrettyTable(headers: string[], rows: string[][]) {
  const allRows = [headers, ...rows]

  // 计算每列最大宽度
  const colWidths = headers.map((_, col) =>
    Math.max(...allRows.map(row => String(row[col]).length))
  )

  // 打印函数
  const formatRow = (row: string[]) =>
    `| ${row.map((cell, i) => pad(String(cell), colWidths[i])).join(' | ')} |`

  console.log(formatRow(headers))
  console.log(
    `| ${colWidths.map(w => '-'.repeat(w)).join(' | ')} |`
  )

  for (const row of rows) {
    console.log(formatRow(row))
  }
}