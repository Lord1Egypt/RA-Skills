/**
 * Base Adapter
 * 
 * All provider adapters extend this class. Provides shared
 * normalisation utilities (date, currency, etc.).
 */

class BaseAdapter {
  constructor(name) {
    this.name = name;
  }

  /**
   * Normalise a date string to ISO YYYY-MM-DD format.
   */
  normaliseDate(dateStr) {
    if (!dateStr) return null;
    // Already ISO
    if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) return dateStr;
    // ISO datetime → date
    if (/^\d{4}-\d{2}-\d{2}T/.test(dateStr)) return dateStr.substring(0, 10);
    // Try parsing
    const parsed = new Date(dateStr);
    if (!isNaN(parsed)) return parsed.toISOString().substring(0, 10);
    return dateStr;
  }

  /**
   * Normalise currency symbol or code to ISO 4217.
   */
  normaliseCurrency(val) {
    if (!val) return null;
    const map = {
      '£': 'GBP', '€': 'EUR', '$': 'USD', '¥': 'JPY', 'CHF': 'CHF',
      'kr': 'SEK', 'zł': 'PLN', 'Kč': 'CZK', 'Fr.': 'CHF',
      'R$': 'BRL', '₹': 'INR', '₽': 'RUB', '₩': 'KRW',
      '₪': 'ILS', '฿': 'THB', '₫': 'VND', '₦': 'NGN',
    };
    return map[val] || val.toUpperCase();
  }

  /**
   * Parse IBAN and BIC from a freeform string.
   */
  parseBankDetailsFromString(str) {
    if (!str) return { iban: null, bic: null };
    const ibanMatch = str.match(/(?:IBAN[:\s]*)?([A-Z]{2}\d{2}[A-Z0-9]{4,30})/i);
    const bicMatch = str.match(/(?:BIC|SWIFT)[:\s]*([A-Z]{6}[A-Z0-9]{2,5})/i);
    return {
      iban: ibanMatch ? ibanMatch[1].replace(/\s/g, '') : null,
      bic: bicMatch ? bicMatch[1] : null,
    };
  }

  /**
   * Normalise a VAT rate value.
   * Handles "20%", "20", 20, 0.2 → 20
   */
  normaliseVatRate(val) {
    if (val === null || val === undefined) return null;
    const str = String(val).replace('%', '').trim();
    const num = parseFloat(str);
    if (isNaN(num)) return null;
    // If < 1, assume it's a decimal (0.2 → 20)
    return num < 1 ? num * 100 : num;
  }

  /**
   * Extract referenced documents from various provider formats.
   */
  extractReferencedDocs(raw) {
    const docs = [];
    const mappings = {
      PO: ['po_number', 'purchaseOrderRef', 'purchase_order', 'poNumber', 'po_ref'],
      contract: ['contract_number', 'contractRef', 'contract_reference', 'contractNumber'],
      GRN: ['grn_number', 'delivery_note', 'deliveryNoteRef', 'grnNumber'],
      inspection: ['inspection_report', 'acceptance_report', 'inspectionRef'],
      timesheet: ['timesheet_ref', 'timesheetNumber', 'timesheet_reference'],
      project: ['project_ref', 'project_number', 'projectCode', 'job_ref'],
      proforma: ['proforma_ref', 'proforma_invoice', 'proformaNumber'],
    };

    for (const [type, keys] of Object.entries(mappings)) {
      for (const key of keys) {
        const val = this._deepGet(raw, key);
        if (val) {
          docs.push({ type, reference: String(val) });
          break;
        }
      }
    }
    return docs;
  }

  /**
   * Deep get a value from nested object by key name (searches recursively).
   */
  _deepGet(obj, key) {
    if (!obj || typeof obj !== 'object') return undefined;
    if (obj[key] !== undefined) return obj[key];
    for (const v of Object.values(obj)) {
      if (typeof v === 'object') {
        const found = this._deepGet(v, key);
        if (found !== undefined) return found;
      }
    }
    return undefined;
  }

  /**
   * Parse a number that might be in any locale format.
   * Handles: 1,234.56 | 1.234,56 | 1 234,56 | 1 234-56 | 1,23,456.78
   * Returns a standard JavaScript number.
   */
  parseLocaleNumber(val) {
    if (val === null || val === undefined) return null;
    if (typeof val === 'number') return val;
    
    let str = String(val).trim();
    if (!str) return null;

    // Remove currency symbols and words
    str = str.replace(/[£$€¥₽₹₩₪฿₫₦]/g, '').trim();
    str = str.replace(/\b(руб|р|RUB|USD|EUR|GBP|CNY|JPY)\b\.?/gi, '').trim();

    // Russian hyphen-as-decimal: "4 631-32" → "4631.32"
    if (/^\d[\d\s]*-\d{1,2}$/.test(str)) {
      str = str.replace(/\s/g, '').replace('-', '.');
      return parseFloat(str);
    }

    // Remove spaces (thousands separator in French/Russian)
    str = str.replace(/\s/g, '');

    // Count dots and commas
    const dots = (str.match(/\./g) || []).length;
    const commas = (str.match(/,/g) || []).length;

    // Determine which is the decimal separator by looking at the LAST separator
    const lastDot = str.lastIndexOf('.');
    const lastComma = str.lastIndexOf(',');

    if (dots === 0 && commas === 0) {
      // Plain integer: "1234"
      return parseFloat(str);
    } else if (dots === 0 && commas === 1) {
      // "1234,56" — comma is decimal
      return parseFloat(str.replace(',', '.'));
    } else if (dots === 1 && commas === 0) {
      // "1234.56" — dot is decimal (standard)
      return parseFloat(str);
    } else if (dots === 0 && commas >= 2) {
      // "1,23,456" — Indian format, all commas are thousands
      return parseFloat(str.replace(/,/g, ''));
    } else if (commas === 0 && dots >= 2) {
      // "1.234.567" — all dots are thousands
      return parseFloat(str.replace(/\./g, ''));
    } else if (lastComma > lastDot) {
      // "1.234,56" — last separator is comma → comma is decimal, dots are thousands
      return parseFloat(str.replace(/\./g, '').replace(',', '.'));
    } else if (lastDot > lastComma) {
      // "1,234.56" or "1,23,456.78" — last separator is dot → dot is decimal, commas are thousands
      return parseFloat(str.replace(/,/g, ''));
    }

    // Fallback
    return parseFloat(str.replace(/[^0-9.\-]/g, '')) || null;
  }

  /**
   * Subclasses must implement this.
   * @param {object} rawResponse - Raw AI provider response
   * @returns {object} Canonical invoice object
   */
  normalise(rawResponse) {
    throw new Error(`${this.name}: normalise() not implemented`);
  }
}

module.exports = { BaseAdapter };
