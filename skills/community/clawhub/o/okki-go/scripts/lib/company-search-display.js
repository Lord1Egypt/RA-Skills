'use strict';

const DISPLAY_FIELDS = [
  'row',
  'company_name',
  'country_name',
  'company_type',
  'fit',
  'has_email',
  'more_info'
];

const HEADERS = {
  en: {
    row: 'Row',
    company_name: 'Company Name',
    country_name: 'Country/Region',
    company_type: 'Company Type',
    fit: 'Fit',
    has_email: 'Has Email',
    more_info: 'More Info'
  },
  zh: {
    row: '序号',
    company_name: '公司名称',
    country_name: '国家/地区',
    company_type: '公司类型',
    fit: '匹配理由',
    has_email: '有邮箱',
    more_info: '更多信息'
  }
};

const DETAIL_LABELS = {
  en: {
    yes: 'Yes',
    no: 'No',
    unknown: 'Unknown',
    whatsapp: 'WhatsApp',
    employees: 'Employees',
    founded: 'Founded',
    nameValueSeparator: ': ',
    itemSeparator: '; '
  },
  zh: {
    yes: '是',
    no: '否',
    unknown: '未知',
    whatsapp: 'WhatsApp',
    employees: '员工数',
    founded: '成立时间',
    nameValueSeparator: '：',
    itemSeparator: '；'
  }
};

const SEPARATOR = '|---:|---|---|---|---|---|---|';

function languageFromLocale(locale) {
  return /^zh\b/i.test(String(locale || '')) ? 'zh' : 'en';
}

function headerForLocale(locale) {
  const labels = HEADERS[languageFromLocale(locale)];
  return `| ${DISPLAY_FIELDS.map((field) => labels[field]).join(' | ')} |`;
}

function markdownCell(value) {
  if (value === null || value === undefined) return '';
  return String(value)
    .replace(/\r?\n/g, ' ')
    .replace(/\s+/g, ' ')
    .replace(/\|/g, '\\|')
    .trim();
}

function localizedValue(value, labels) {
  if (value === true) return labels.yes;
  if (value === false) return labels.no;
  if (value === null || value === undefined || value === '') return labels.unknown;
  if (String(value).trim() === '未知') return labels.unknown;
  if (String(value).trim().toLowerCase() === 'unknown') return labels.unknown;
  return value;
}

function displayRow(row, labels) {
  return {
    row: row.row,
    company_name: row.company_name,
    country_name: row.country_name,
    company_type: row.company_type,
    fit: row.fit,
    has_email: localizedValue(row.has_email, labels),
    more_info: [
      `${labels.whatsapp}${labels.nameValueSeparator}${localizedValue(row.has_whatsapp, labels)}`,
      `${labels.employees}${labels.nameValueSeparator}${localizedValue(row.employees_count, labels)}`,
      `${labels.founded}${labels.nameValueSeparator}${localizedValue(row.founding_time, labels)}`
    ].join(labels.itemSeparator)
  };
}

function renderCompanySearchTable(rows, options = {}) {
  const list = Array.isArray(rows) ? rows : [];
  const language = languageFromLocale(options.locale);
  const lines = [headerForLocale(options.locale), SEPARATOR];
  for (const row of list) {
    const formatted = displayRow(row, DETAIL_LABELS[language]);
    lines.push(`| ${DISPLAY_FIELDS.map((field) => markdownCell(formatted[field])).join(' | ')} |`);
  }
  return lines.join('\n');
}

function addCompanySearchDisplayTable(output, options = {}) {
  if (!output || typeof output !== 'object') return output;
  const { display_rows: displayRows, ...normalOutput } = output;
  return {
    ...normalOutput,
    display_table_markdown: renderCompanySearchTable(displayRows || normalOutput.rows, options)
  };
}

module.exports = {
  DISPLAY_FIELDS,
  addCompanySearchDisplayTable,
  renderCompanySearchTable
};
