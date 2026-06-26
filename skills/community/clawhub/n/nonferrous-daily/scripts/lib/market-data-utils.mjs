function toNumber(value) {
  if (value == null) return null;
  const normalized = String(value).replace(/,/g, '').trim();
  if (!normalized) return null;
  const number = Number.parseFloat(normalized);
  return Number.isFinite(number) ? number : null;
}

function stripHtml(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, '\n')
    .replace(/&nbsp;/gi, ' ')
    .replace(/\r/g, '')
    .replace(/\u00a0/g, ' ')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n+/g, '\n');
}

export function parseShfeInventoryHtml(html, metal) {
  const text = stripHtml(html);
  const latestMatch = text.match(/最新数据[\s\S]*?(\d{4}\s*W\d{2})[\s\S]*?([\d,]+(?:\.\d+)?)\s*[\r\n]+([\d,]+(?:\.\d+)?)/);
  if (!latestMatch) {
    throw new Error(`No weekly inventory block found for ${metal}`);
  }

  const weekLabel = latestMatch[1].replace(/\s+/g, ' ').trim();
  const tonnes = toNumber(latestMatch[2]);
  const previous = toNumber(latestMatch[3]);
  if (tonnes == null || previous == null) {
    throw new Error(`Invalid weekly inventory values for ${metal}`);
  }

  return {
    tonnes: Math.round(tonnes),
    change: Math.round(tonnes - previous),
    unit: 'tonnes',
    dataDate: weekLabel,
    weekLabel,
    source: 'SHFE/MacroMicro',
  };
}

export function buildInventorySnapshot(lmeInventory, shfeInventory) {
  return {
    copper: lmeInventory?.copper ?? null,
    zinc: lmeInventory?.zinc ?? null,
    nickel: lmeInventory?.nickel ?? null,
    cobalt: lmeInventory?.cobalt ?? null,
    note: lmeInventory?.note ?? null,
    lme: {
      copper: lmeInventory?.copper ?? null,
      zinc: lmeInventory?.zinc ?? null,
      nickel: lmeInventory?.nickel ?? null,
    },
    shfe: {
      copper: shfeInventory?.copper ?? null,
      zinc: shfeInventory?.zinc ?? null,
      nickel: shfeInventory?.nickel ?? null,
    },
  };
}

export function buildMagnesiumPrice(ccmnData, usdCny) {
  const magnesium = ccmnData?.magnesium;
  if (!magnesium) {
    return { cny: null, usdEstimate: null, source: null };
  }

  const fx = usdCny?.price;
  const usdEstimate = fx && fx > 0 ? Math.round(magnesium.price / fx) : null;

  return {
    cny: magnesium.price ?? null,
    cnyChange: magnesium.updown ?? null,
    cnyUnit: '元/吨',
    usdEstimate,
    usdUnit: 'USD/t',
    usdSource: usdEstimate != null ? 'CCMN/FX-estimate' : null,
    dataDate: ccmnData?.dataDate ?? null,
    source: 'CCMN',
  };
}
