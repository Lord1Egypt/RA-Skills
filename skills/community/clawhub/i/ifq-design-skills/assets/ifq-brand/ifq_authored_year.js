(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module.exports) {
    module.exports = api;
  }
  root.IfqAuthoredYear = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  const token = '__IFQ_YEAR__';
  const yearMonthToken = '__IFQ_YEAR_MONTH__';
  const dateToken = '__IFQ_DATE__';
  const isoDateToken = '__IFQ_ISO_DATE__';

  function pad(value) {
    return String(value).padStart(2, '0');
  }

  function fromDateValue(value) {
    if (value instanceof Date) {
      if (Number.isNaN(value.getTime())) {
        return null;
      }

      return value;
    }

    if (typeof value === 'number' && Number.isFinite(value)) {
      const authoredDate = new Date(value);
      if (Number.isNaN(authoredDate.getTime())) {
        return null;
      }

      return authoredDate;
    }

    return null;
  }

  function fromDateParts(year, month, day) {
    const parsedYear = Number.parseInt(year, 10);
    const parsedMonth = Number.parseInt(month, 10);
    const parsedDay = Number.parseInt(day, 10);

    if (!Number.isInteger(parsedYear) || !Number.isInteger(parsedMonth) || !Number.isInteger(parsedDay)) {
      return null;
    }

    const authoredDate = new Date(parsedYear, parsedMonth - 1, parsedDay);
    if (Number.isNaN(authoredDate.getTime())) {
      return null;
    }

    if (
      authoredDate.getFullYear() !== parsedYear
      || authoredDate.getMonth() !== parsedMonth - 1
      || authoredDate.getDate() !== parsedDay
    ) {
      return null;
    }

    return authoredDate;
  }

  function fromStringValue(value) {
    if (typeof value !== 'string') {
      return null;
    }

    const normalized = value.trim();
    if (!normalized) {
      return null;
    }

    if (/^\d{4}$/.test(normalized)) {
      return fromDateParts(normalized, 1, 1);
    }

    if (/^\d{10}$/.test(normalized) || /^\d{13}$/.test(normalized)) {
      const numericDate = fromDateValue(Number(normalized));
      if (numericDate) {
        return numericDate;
      }
    }

    const isoMatch = normalized.match(/^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})(?:\b|T|\s|$)/);
    if (isoMatch) {
      const isoDate = fromDateParts(isoMatch[1], isoMatch[2], isoMatch[3]);
      if (isoDate) {
        return isoDate;
      }
    }

    const usMatch = normalized.match(/^(\d{1,2})[/-](\d{1,2})[/-](\d{4})(?:\b|\s|$)/);
    if (usMatch) {
      const usDate = fromDateParts(usMatch[3], usMatch[1], usMatch[2]);
      if (usDate) {
        return usDate;
      }
    }

    const parsedTimestamp = Date.parse(normalized);
    if (Number.isFinite(parsedTimestamp)) {
      return fromDateValue(parsedTimestamp);
    }

    return null;
  }

  function resolveInfo(lastModified) {
    const authoredDate = fromDateValue(lastModified) || fromStringValue(lastModified) || new Date();
    const year = String(authoredDate.getFullYear());
    const month = pad(authoredDate.getMonth() + 1);
    const day = pad(authoredDate.getDate());

    return {
      year,
      month,
      day,
      yearMonth: `${year} · ${month}`,
      date: `${year} · ${month} · ${day}`,
      isoDate: `${year}-${month}-${day}`,
    };
  }

  function resolve(lastModified) {
    return resolveInfo(lastModified).year;
  }

  function resolveSource(doc) {
    if (!doc) {
      return undefined;
    }

    const rootValue = doc.documentElement && doc.documentElement.getAttribute('data-ifq-created-at');
    if (typeof rootValue === 'string' && rootValue.trim()) {
      return rootValue;
    }

    const meta = typeof doc.querySelector === 'function'
      ? doc.querySelector('meta[name="ifq-created-at"], meta[name="ifq:created-at"]')
      : null;
    if (meta && typeof meta.content === 'string' && meta.content.trim()) {
      return meta.content;
    }

    return doc.lastModified;
  }

  function replaceNodeText(node, fallbackValue, replacements) {
    const originalText = typeof node.textContent === 'string' ? node.textContent : '';
    let nextText = originalText;

    replacements.forEach((replacement, search) => {
      nextText = nextText.split(search).join(replacement);
    });

    if (nextText === originalText) {
      nextText = fallbackValue;
    }

    node.textContent = nextText;

    if (node.tagName === 'TIME' && replacements.has(isoDateToken)) {
      node.setAttribute('datetime', replacements.get(isoDateToken));
    }
  }

  function formatDate(info, format) {
    switch (format) {
      case 'iso':
        return info.isoDate;
      case 'year':
        return info.year;
      case 'year-month':
        return info.yearMonth;
      default:
        return info.date;
    }
  }

  function apply(doc) {
    const targetDocument = doc && typeof doc.querySelectorAll === 'function'
      ? doc
      : root.document && typeof root.document.querySelectorAll === 'function'
        ? root.document
        : null;
    const info = resolveInfo(resolveSource(targetDocument));
    const replacements = new Map([
      [token, info.year],
      [yearMonthToken, info.yearMonth],
      [dateToken, info.date],
      [isoDateToken, info.isoDate],
    ]);

    if (!targetDocument) {
      return info.year;
    }

    targetDocument.querySelectorAll('[data-ifq-authored-year]').forEach((node) => {
      replaceNodeText(node, info.year, replacements);
    });

    targetDocument.querySelectorAll('[data-ifq-authored-date]').forEach((node) => {
      replaceNodeText(node, formatDate(info, node.getAttribute('data-ifq-authored-date')), replacements);
    });

    return info.year;
  }

  return {
    token,
    yearMonthToken,
    dateToken,
    isoDateToken,
    resolve,
    resolveInfo,
    apply,
  };
});