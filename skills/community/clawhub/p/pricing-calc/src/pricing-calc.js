/**
 * PricingCalc — Product & Service Pricing Calculator
 * @author @TheShadowRose
 * @license MIT
 */

class PricingCalc {
  serviceRate({ annualTarget, workWeeks = 48, billableHours = 25, expenses = 0, taxRate = 0.25 }) {
    if (!workWeeks || !billableHours) return { error: 'workWeeks and billableHours must be > 0' };
    if (taxRate >= 1) return { error: 'taxRate must be less than 1' };
    const grossNeeded = (annualTarget + expenses) / (1 - taxRate);
    const totalHours = workWeeks * billableHours;
    const minimum = Math.ceil(grossNeeded / totalHours);
    const recommended = Math.ceil(minimum * 1.2); // 20% buffer
    return { minimum, recommended, totalHours, grossNeeded: Math.round(grossNeeded) };
  }

  productPrice({ costPerUnit, targetMargin, competitors = [], positioning = 'mid' }) {
    const costBased = costPerUnit / (1 - targetMargin);
    let marketBased = costBased;
    if (competitors.length > 0) {
      const sorted = [...competitors].sort((a, b) => a - b);
      const positions = { low: 0.25, mid: 0.5, premium: 0.75 };
      const idx = Math.floor(sorted.length * (positions[positioning] || 0.5));
      marketBased = sorted[Math.min(idx, sorted.length - 1)];
    }
    const recommended = Math.round(Math.max(costBased, marketBased * 0.9) * 100) / 100;
    const actualMargin = ((recommended - costPerUnit) / recommended * 100).toFixed(1);
    return { recommended, costBased: Math.round(costBased * 100) / 100, marketBased, actualMargin: actualMargin + '%' };
  }

  breakEven({ fixedCosts, pricePerUnit, costPerUnit }) {
    const margin = pricePerUnit - costPerUnit;
    if (margin <= 0) return { units: null, error: true, message: 'Price must exceed cost per unit' };
    const units = Math.ceil(fixedCosts / margin);
    return { units, revenue: units * pricePerUnit, margin: margin.toFixed(2) };
  }

  tieredPricing({ basePrice, tiers = 3, multipliers }) {
    const defaults = { 3: [1, 1.8, 3], 4: [1, 1.6, 2.5, 4] };
    const mults = multipliers || defaults[tiers] || defaults[3];
    return mults.map((m, i) => ({
      tier: i + 1,
      name: ['Basic', 'Pro', 'Enterprise', 'Custom'][i] || `Tier ${i+1}`,
      price: Math.round(basePrice * m * 100) / 100,
      multiplier: m
    }));
  }

  discountImpact({ basePrice, discountPercent, baseCost }) {
    if (discountPercent >= 100) return { error: 'Discount cannot be 100% or more' };
    const discounted = basePrice * (1 - discountPercent / 100);
    const baseMargin = ((basePrice - baseCost) / basePrice * 100).toFixed(1);
    const newMargin = ((discounted - baseCost) / discounted * 100).toFixed(1);
    const volumeNeeded = Math.ceil(basePrice / discounted * 100) / 100;
    return {
      discountedPrice: discounted.toFixed(2),
      baseMargin: baseMargin + '%',
      newMargin: newMargin + '%',
      volumeMultiplier: volumeNeeded,
      message: `Need ${(volumeNeeded * 100 - 100).toFixed(0)}% more sales to match base revenue`
    };
  }
}

module.exports = { PricingCalc };
