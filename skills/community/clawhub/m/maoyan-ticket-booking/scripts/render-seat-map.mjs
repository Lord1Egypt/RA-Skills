#!/usr/bin/env node
/**
 * render-seat-map.mjs — 以指定座位为中心渲染座位图
 *
 * Input（JSON，通过 stdin 传入）：
 * {
 *   rows: Array<{           // 座位图整体数据（来自 get-seat-map.mjs 返回的 regions[0].rows）
 *     rowId: string,
 *     rowNum: string,
 *     seats: Array<{
 *       seatNo: string,
 *       rowId: string,
 *       columnId: string,
 *       seatStatus: number,  // 0=过道, 1=可售, 2=锁定, 3=售出, 4=禁售
 *       seatType: string,
 *       price: number,
 *       sectionName: string
 *     }>
 *   }>,
 *   centerSeats: Array<{    // 中心座位列表（支持多个）
 *     rowId: string,        // 座位行ID
 *     columnId: string,     // 座位列ID
 *     mark?: string         // 可选，自定义标记符号（默认 ★）
 *   }>,
 *   rowRange: number,       // 可选，上下显示行数，默认 3（即共7行）
 *   colRange: number        // 可选，左右显示列数，默认 5（即共11列）
 * }
 */

// 座位状态符号映射
const SEAT_SYMBOLS = {
  0: ' ',  // 过道/空白区域
  1: '○', // 可售
  2: '×', // 已锁定
  3: '●', // 已售出
  4: '■', // 禁售
};

// 默认标记符号（所有选中座位统一用★）
const DEFAULT_MARK = '★';

// 座位图最大显示宽度（字符数），避免太宽导致显示问题
const MAX_DISPLAY_WIDTH = 60;
// 最多显示的座位数
const MAX_SEATS_COUNT = 12;

/**
 * 读取标准输入
 */
async function readStdin() {
  let data = '';
  process.stdin.setEncoding('utf8');
  for await (const chunk of process.stdin) {
    data += chunk;
  }
  return JSON.parse(data);
}

/**
 * 以指定座位为中心渲染座位图（支持多个中心座位）
 */
function renderSeatMap(rows, centerSeats, rowRange = 3, colRange = 5, headerLabel = '已选座位') {
  if (!rows || rows.length === 0) {
    return { error: '座位数据为空' };
  }

  if (!centerSeats || centerSeats.length === 0) {
    return { error: '缺少 centerSeats 参数' };
  }

  // 验证并修正 rowRange/colRange，确保为正数
  rowRange = Math.max(0, Math.floor(Number(rowRange) || 3));
  colRange = Math.max(0, Math.floor(Number(colRange) || 5));

  // 标准化中心座位数据，分配标记符号
  const normalizedCenters = centerSeats.map((seat, index) => ({
    rowId: seat.rowId,
    columnId: seat.columnId,
    mark: seat.mark || DEFAULT_MARK,
    index: index + 1,
  }));

  // 查找所有中心座位在 rows 中的位置
  const centerPositions = [];
  for (const center of normalizedCenters) {
    const rowIndex = rows.findIndex(r => r.rowId === center.rowId);
    if (rowIndex === -1) {
      return { error: `未找到行ID: ${center.rowId}` };
    }

    const row = rows[rowIndex];
    const colIndex = row.seats.findIndex(s => s.columnId === center.columnId);
    if (colIndex === -1) {
      return { error: `未找到列ID: ${center.columnId}（行: ${center.rowId}）` };
    }

    centerPositions.push({
      ...center,
      rowIndex,
      colIndex,
      rowNum: row.rowNum,
      seatNo: row.seats[colIndex].seatNo,
      seatStatus: row.seats[colIndex].seatStatus,
      price: row.seats[colIndex].price,
    });
  }

  // 计算显示范围：以第一个中心座位为基准，加上其他座位的范围
  const primaryCenter = centerPositions[0];

  // 计算所有中心座位覆盖的范围
  const allRowIndices = centerPositions.map(p => p.rowIndex);
  const allColIndices = centerPositions.map(p => p.colIndex);

  const minCenterRow = Math.min(...allRowIndices);
  const maxCenterRow = Math.max(...allRowIndices);
  const minCenterCol = Math.min(...allColIndices);
  const maxCenterCol = Math.max(...allColIndices);

  // 计算显示边界
  const startRowIndex = Math.max(0, minCenterRow - rowRange);
  const endRowIndex = Math.min(rows.length - 1, maxCenterRow + rowRange);

  // 计算列范围的基准（不再假设每行列数相同）
  let baseStartCol = Math.max(0, minCenterCol - colRange);
  let baseEndCol = maxCenterCol + colRange;

  // 限制最大显示宽度，避免座位图太宽
  const rowPrefixWidth = 4;  // "XX排 " 占4字符
  let currentWidth = baseEndCol - baseStartCol + 1;

  if (currentWidth > MAX_SEATS_COUNT) {
    // 超过最大座位数，以中心座位为基准进行裁剪
    const halfWidth = Math.floor(MAX_SEATS_COUNT / 2);
    const primaryCenterCol = centerPositions[0].colIndex;
    baseStartCol = Math.max(0, primaryCenterCol - halfWidth);
    baseEndCol = baseStartCol + MAX_SEATS_COUNT - 1;

    // 确保所有中心座位都在显示范围内
    const needsLeftShift = minCenterCol < baseStartCol;
    const needsRightShift = maxCenterCol > baseEndCol;

    if (needsLeftShift || needsRightShift) {
      if (needsLeftShift && needsRightShift) {
        // 中心座位范围本身就超过最大宽度，先左对齐再右对齐，尽量包含更多中心座位
        baseStartCol = Math.max(0, minCenterCol);
        baseEndCol = baseStartCol + MAX_SEATS_COUNT - 1;
        if (baseEndCol < maxCenterCol) {
          baseEndCol = maxCenterCol;
          baseStartCol = Math.max(0, baseEndCol - MAX_SEATS_COUNT + 1);
        }
      } else if (needsLeftShift) {
        // 需要向左移
        const shift = baseStartCol - minCenterCol;
        baseStartCol = Math.max(0, baseStartCol - shift);
        baseEndCol = baseStartCol + MAX_SEATS_COUNT - 1;
      } else {
        // 需要向右移
        const shift = maxCenterCol - baseEndCol;
        baseEndCol = baseEndCol + shift;
        baseStartCol = Math.max(0, baseEndCol - MAX_SEATS_COUNT + 1);
      }
    }
  }

  // 创建中心座位查找表
  const centerSeatMap = new Map();
  for (const pos of centerPositions) {
    centerSeatMap.set(`${pos.rowIndex}-${pos.colIndex}`, pos.mark);
  }

  // 生成座位图文本
  const lines = [];

  // 计算实际显示的最大列数（遍历所有要显示的行）
  let maxSeatCount = 0;
  for (let i = startRowIndex; i <= endRowIndex; i++) {
    const seats = rows[i]?.seats || [];
    const rowEndCol = Math.min(baseEndCol, seats.length - 1);
    const rowSeatCount = rowEndCol >= baseStartCol ? rowEndCol - baseStartCol + 1 : 0;
    maxSeatCount = Math.max(maxSeatCount, rowSeatCount);
  }

  // 顶部银幕标识（宽度与座位图对齐）
  // 座位图每行格式: "XX排 ○○○..." = 4字符行号 + seatCount字符座位（无空格）
  const seatCount = maxSeatCount > 0 ? maxSeatCount : (baseEndCol - baseStartCol + 1);
  const seatsWidth = seatCount;  // 每个座位占1字符（无空格）
  const screenPadding = 3;  // 银幕行前面的空格
  // 确保银幕宽度不为负数
  const screenWidth = Math.max(0, Math.floor((rowPrefixWidth + seatsWidth - 6) / 2));  // 银幕两侧等号数量（减去" 银幕 "6字符）

  if (screenWidth > 0) {
    lines.push(' '.repeat(screenPadding) + '═'.repeat(screenWidth) + ' 银幕 ' + '═'.repeat(screenWidth));
  } else {
    lines.push(' '.repeat(screenPadding) + ' 银幕 ');
  }
  lines.push('');

  // 第一行：显示选中座位信息
  const seatInfoList = centerPositions.map(p => `${p.rowNum}排${p.columnId}座`).join('、');
  lines.push(`${headerLabel}：${seatInfoList}（共${centerPositions.length}座）`);
  lines.push('');

  // 生成每一行
  for (let i = startRowIndex; i <= endRowIndex; i++) {
    const row = rows[i];
    const seats = row.seats || [];

    // 计算该行实际的列范围
    const rowStartCol = baseStartCol;
    const rowEndCol = Math.min(baseEndCol, seats.length - 1);

    // 行号（右对齐）
    const rowNumStr = String(row.rowNum).padStart(2, ' ');
    let rowText = `${rowNumStr}排 `;

    // 如果该行没有在显示范围内的座位，添加提示
    if (rowEndCol < rowStartCol || seats.length === 0) {
      rowText += '（无座位）';
    } else {
      for (let j = rowStartCol; j <= rowEndCol && j < seats.length; j++) {
        const seat = seats[j];
        const centerMark = centerSeatMap.get(`${i}-${j}`);

        if (centerMark) {
          // 中心座位用特殊标记
          rowText += centerMark;
        } else {
          // 验证 seatStatus，未知状态使用空格
          const status = seat?.seatStatus;
          rowText += SEAT_SYMBOLS[status] ?? ' ';
        }
        // 符号之间不加空格
      }
    }

    // 标记包含中心座位的行
    const centersInRow = centerPositions.filter(p => p.rowIndex === i);
    if (centersInRow.length > 0) {
      rowText += ` ← ${headerLabel}`;
    }

    lines.push(rowText);
  }

  // 座位图说明
  lines.push('');
  lines.push('座位符号：○可售 ×已锁定 ●已售出 ■禁售 ★已选中');

  // 显示选中座位列表
  lines.push('');
  lines.push(`${headerLabel}：`);
  for (const pos of centerPositions) {
    lines.push(`  ${pos.mark} = ${pos.rowNum}排${pos.columnId}座 (${pos.seatNo})`);
  }

  return {
    seatMapText: lines.join('\n'),
    centerSeats: centerPositions.map(p => ({
      rowId: p.rowId,
      rowNum: p.rowNum,
      columnId: p.columnId,
      seatNo: p.seatNo,
      seatStatus: p.seatStatus,
      price: p.price,
      mark: p.mark,
    })),
    displayRange: {
      rows: { start: startRowIndex, end: endRowIndex },
      cols: { start: baseStartCol, end: baseEndCol },
      primaryCenter: { rowIndex: primaryCenter.rowIndex, colIndex: primaryCenter.colIndex },
    },
  };
}

// 主函数
async function main() {
  try {
    const input = await readStdin();

    // 参数校验
    if (!input.rows) {
      console.error(JSON.stringify({ error: '缺少 rows 参数' }));
      process.exit(1);
    }
    if (!input.centerSeats || !Array.isArray(input.centerSeats) || input.centerSeats.length === 0) {
      console.error(JSON.stringify({ error: '缺少 centerSeats 参数（必须是数组）' }));
      process.exit(1);
    }

    const result = renderSeatMap(
      input.rows,
      input.centerSeats,
      input.rowRange,
      input.colRange
    );

    if (result.error) {
      console.error(JSON.stringify({ error: result.error }));
      process.exit(1);
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (e) {
    console.error(JSON.stringify({ error: e.message }));
    process.exit(1);
  }
}

// 只在直接运行时才调用 main()
if (import.meta.url === new URL(process.argv[1], 'file://').href) {
  main();
}

export { renderSeatMap };
