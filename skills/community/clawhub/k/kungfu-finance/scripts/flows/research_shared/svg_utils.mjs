function toNumber(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

export function escapeXml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

export function formatDateLabel(value) {
  const raw = String(value ?? "").trim();

  if (!/^\d{8}$/u.test(raw)) {
    return raw || "未知日期";
  }

  return `${raw.slice(0, 4)}.${raw.slice(4, 6)}.${raw.slice(6, 8)}`;
}

export function buildDateRangeLabel(start, end) {
  const startLabel = formatDateLabel(start);
  const endLabel = end ? formatDateLabel(end) : "?";
  return `${startLabel}-${endLabel}`;
}

export function extent(values) {
  const numericValues = values.map(toNumber).filter((item) => item !== null);

  if (!numericValues.length) {
    return {
      min: 0,
      max: 1
    };
  }

  const min = Math.min(...numericValues);
  const max = Math.max(...numericValues);

  if (min === max) {
    return {
      min: min - 1,
      max: max + 1
    };
  }

  return {
    min,
    max
  };
}

export function scaleValue(value, range, {
  yTop,
  yBottom
}) {
  const numericValue = toNumber(value);

  if (numericValue === null) {
    return yBottom;
  }

  const ratio = (range.max - numericValue) / (range.max - range.min);
  return Number((yTop + ratio * (yBottom - yTop)).toFixed(2));
}

export function buildPolylinePoints(values, {
  xStart,
  xEnd,
  yTop,
  yBottom
}) {
  const numericValues = values.map(toNumber);
  const range = extent(numericValues);
  const denominator = Math.max(numericValues.length - 1, 1);

  return numericValues
    .map((value, index) => {
      const x = xStart + ((xEnd - xStart) * index) / denominator;
      const y = scaleValue(value, range, {
        yTop,
        yBottom
      });
      return `${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");
}

export function buildChartPoint(value, index, total, {
  xStart,
  xEnd,
  yTop,
  yBottom,
  range
}) {
  const denominator = Math.max(total - 1, 1);
  const x = xStart + ((xEnd - xStart) * index) / denominator;
  const y = scaleValue(value, range, {
    yTop,
    yBottom
  });

  return {
    x: Number(x.toFixed(2)),
    y
  };
}

export function buildStars({
  width,
  height,
  count = 5
}) {
  const stars = [];

  for (let index = 0; index < count; index += 1) {
    const x = 40 + ((width - 80) / Math.max(count - 1, 1)) * index;
    const y = 26 + (index % 2) * 18;
    stars.push(
      `<circle cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="1.8" fill="#ffffff" opacity="0.15"/>`
    );
  }

  return stars.join("\n");
}

export function buildStageLabel({
  x,
  y,
  title,
  isFuture = false
}) {
  return `<text x="${x}" y="${y}" fill="${isFuture ? "#94a3b8" : "#e2e8f0"}" font-size="10" font-weight="700" text-anchor="middle" opacity="${isFuture ? "0.75" : "1"}">${escapeXml(title)}</text>`;
}

export function buildDivider({
  x,
  y1,
  y2,
  future = false
}) {
  return `<line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" stroke="${future ? "#64748b" : "#475569"}" stroke-width="1.2" stroke-dasharray="${future ? "5,5" : "0"}" opacity="0.7"/>`;
}

export function buildBubble({
  x,
  y,
  width,
  height,
  title,
  lines,
  stroke
}) {
  const textLines = [title, ...lines]
    .map((line, index) => `<text x="${x + 10}" y="${y + 16 + index * 12}" fill="#e2e8f0" font-size="${index === 0 ? 10 : 9}" font-weight="${index === 0 ? 700 : 500}">${escapeXml(line)}</text>`)
    .join("\n");

  return `<g class="data-bubble"><rect x="${x}" y="${y}" width="${width}" height="${height}" rx="8" fill="rgba(15,23,42,0.82)" stroke="${stroke}" stroke-width="1.2"/>${textLines}</g>`;
}

export function inferProjectionValue(currentValue, direction, {
  up = 0.08,
  flat = 0.02,
  down = -0.08
} = {}) {
  const numericValue = toNumber(currentValue) ?? 0;
  const ratio = direction === "up" ? up : direction === "down" ? down : flat;
  return Number((numericValue * (1 + ratio)).toFixed(2));
}
