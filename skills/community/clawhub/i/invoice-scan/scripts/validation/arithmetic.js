/**
 * Arithmetic Validation
 * 
 * Validates that invoice numbers add up correctly:
 * - Line items sum to net total
 * - Tax calculations are correct
 * - Net + tax = gross
 */

const TOLERANCE = 0.02; // 2p tolerance for rounding
const ROUNDING_THRESHOLD = 1.00; // discrepancies ≤ this are warnings, not errors

/**
 * Validate arithmetic consistency of an invoice.
 * Mutates invoice.validation in place.
 * 
 * @param {object} invoice - Canonical invoice object
 * @returns {object} invoice - Same object with validation populated
 */
function validateArithmetic(invoice) {
  const errors = [];
  const warnings = [];

  // 1. Line items sum → net total
  if (invoice.lineItems.length > 0 && invoice.totals.netTotal !== null) {
    const lineSum = invoice.lineItems.reduce((sum, li) => {
      return sum + (li.lineTotal || 0);
    }, 0);

    const lineSumDiff = Math.abs(lineSum - invoice.totals.netTotal);
    if (lineSumDiff > TOLERANCE) {
      const entry = {
        field: 'totals.netTotal',
        message: `Line items sum (${lineSum.toFixed(2)}) does not match net total (${invoice.totals.netTotal.toFixed(2)})`,
      };
      if (lineSumDiff <= ROUNDING_THRESHOLD) {
        entry.message += ' (likely rounding)';
        warnings.push(entry);
      } else {
        errors.push(entry);
      }
    }
  }

  // 2. Individual line item: qty × price = line total
  invoice.lineItems.forEach((li, i) => {
    if (li.quantity !== null && li.unitPrice !== null && li.lineTotal !== null) {
      const expected = li.quantity * li.unitPrice;
      // Account for discounts
      const afterDiscount = li.discount ? expected - li.discount : expected;
      const liDiff = Math.abs(afterDiscount - li.lineTotal);
      if (liDiff > TOLERANCE) {
        const entry = {
          field: `lineItems[${i}].lineTotal`,
          message: `qty (${li.quantity}) × price (${li.unitPrice}) = ${expected.toFixed(2)}, but lineTotal is ${li.lineTotal.toFixed(2)}`,
        };
        if (liDiff <= ROUNDING_THRESHOLD) {
          entry.message += ' (likely rounding)';
          warnings.push(entry);
        } else {
          errors.push(entry);
        }
      }
    }
  });

  // 3. VAT calculation
  if (invoice.totals.netTotal !== null && invoice.totals.vatTotal !== null) {
    // Check against VAT breakdown if available
    if (invoice.totals.vatBreakdown.length > 0) {
      const breakdownSum = invoice.totals.vatBreakdown.reduce((sum, vb) => sum + vb.amount, 0);
      if (Math.abs(breakdownSum - invoice.totals.vatTotal) > TOLERANCE) {
        errors.push({
          field: 'totals.vatTotal',
          message: `VAT breakdown sum (${breakdownSum.toFixed(2)}) does not match vatTotal (${invoice.totals.vatTotal.toFixed(2)})`,
        });
      }
    }

    // If single VAT rate, check the math
    if (invoice.totals.vatBreakdown.length === 1) {
      const rate = invoice.totals.vatBreakdown[0].rate;
      if (rate) {
        const expectedVat = invoice.totals.netTotal * (rate / 100);
        if (Math.abs(expectedVat - invoice.totals.vatTotal) > TOLERANCE) {
          warnings.push({
            field: 'totals.vatTotal',
            message: `Expected VAT at ${rate}% = ${expectedVat.toFixed(2)}, got ${invoice.totals.vatTotal.toFixed(2)}`,
          });
        }
      }
    }
  }

  // 4. Net + VAT = Gross
  if (invoice.totals.netTotal !== null && invoice.totals.vatTotal !== null && invoice.totals.grossTotal !== null) {
    const expectedGross = invoice.totals.netTotal + invoice.totals.vatTotal;
    // Account for invoice-level discount if present
    const discount = invoice.totals.discount || 0;
    const adjustedExpected = expectedGross - discount;
    const grossDiff = Math.abs(adjustedExpected - invoice.totals.grossTotal);
    if (grossDiff > TOLERANCE) {
      const entry = {
        field: 'totals.grossTotal',
        message: `net (${invoice.totals.netTotal.toFixed(2)}) + VAT (${invoice.totals.vatTotal.toFixed(2)})${discount ? ` - discount (${discount.toFixed(2)})` : ''} = ${adjustedExpected.toFixed(2)}, but gross is ${invoice.totals.grossTotal.toFixed(2)}`,
      };
      if (grossDiff <= ROUNDING_THRESHOLD) {
        entry.message += ' (likely rounding)';
        warnings.push(entry);
      } else {
        errors.push(entry);
      }
    }
  }

  // 5. Basic sanity checks
  if (invoice.totals.grossTotal !== null && invoice.totals.netTotal !== null) {
    if (invoice.totals.grossTotal < invoice.totals.netTotal) {
      warnings.push({
        field: 'totals.grossTotal',
        message: 'Gross total is less than net total — possible negative tax or error',
      });
    }
  }

  // 6. amountDue = grossTotal - amountPaid (when all present)
  if (invoice.totals.amountDue !== null && invoice.totals.grossTotal !== null && invoice.totals.amountPaid !== null) {
    const expectedDue = invoice.totals.grossTotal - Math.abs(invoice.totals.amountPaid);
    if (Math.abs(expectedDue - invoice.totals.amountDue) > TOLERANCE) {
      warnings.push({
        field: 'totals.amountDue',
        message: `gross (${invoice.totals.grossTotal.toFixed(2)}) - paid (${Math.abs(invoice.totals.amountPaid).toFixed(2)}) = ${expectedDue.toFixed(2)}, but amountDue is ${invoice.totals.amountDue.toFixed(2)}`,
      });
    }
  }

  // 7. amountPaid > grossTotal warning (overpayment)
  if (invoice.totals.amountPaid !== null && invoice.totals.grossTotal !== null) {
    if (Math.abs(invoice.totals.amountPaid) > invoice.totals.grossTotal + TOLERANCE) {
      warnings.push({
        field: 'totals.amountPaid',
        message: `Amount paid (${Math.abs(invoice.totals.amountPaid).toFixed(2)}) exceeds gross total (${invoice.totals.grossTotal.toFixed(2)}) — possible overpayment or credit`,
      });
    }
  }

  invoice.validation.arithmeticValid = errors.length === 0;
  invoice.validation.errors.push(...errors);
  invoice.validation.warnings.push(...warnings);

  return invoice;
}

module.exports = { validateArithmetic, TOLERANCE };
