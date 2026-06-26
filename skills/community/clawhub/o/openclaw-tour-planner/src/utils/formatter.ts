import { Itinerary, DayPlan, BudgetBreakdown, WeatherForecast, WeatherDay } from '../types';

/**
 * Format a complete itinerary as Markdown — ready to send to a user.
 */
export function formatItinerary(itinerary: Itinerary): string {
  const { destination, durationDays, startDate, endDate, budget, days } = itinerary;

  const parts: string[] = [
    `# 🧭 ${durationDays}-Day ${destination.name} Itinerary`,
    '',
    '## Overview',
    `- **Destination:** ${destination.name}${destination.country ? `, ${destination.country}` : ''}`,
    `- **Dates:** ${formatDate(startDate)} – ${formatDate(endDate)}`,
    itinerary.weatherForecast
      ? `- **Weather:** ${itinerary.weatherForecast.summary}`
      : '',
    `- **Budget estimate:** ${formatCurrency(budget.total.min, budget.currency)} – ${formatCurrency(budget.total.max, budget.currency)}`,
    '',
  ].filter(l => l !== null);

  for (const day of days) {
    parts.push(formatDay(day));
  }

  parts.push(formatBudget(budget));

  if (itinerary.packingList.length) {
    parts.push('## 🎒 Packing List');
    itinerary.packingList.forEach(item => parts.push(`- ${item}`));
    parts.push('');
  }

  if (itinerary.culturalTips.length) {
    parts.push('## 🌏 Cultural Tips');
    itinerary.culturalTips.forEach(tip => parts.push(`- ${tip}`));
    parts.push('');
  }

  const e = itinerary.emergencyInfo;
  parts.push(
    '## 🆘 Emergency Numbers',
    `- Police: **${e.police}**`,
    `- Ambulance: **${e.ambulance}**`,
    e.embassy ? `- Embassy: **${e.embassy}**` : '',
    '',
  );

  return parts.filter(l => l !== null).join('\n');
}

/**
 * Format a single day as a Markdown block.
 */
export function formatDay(day: DayPlan): string {
  const lines: string[] = [
    `## Day ${day.day} — ${day.date} · ${day.theme}`,
  ];

  if (day.weather) {
    lines.push(`*${formatWeatherLine(day.weather)}*`);
  }
  lines.push('');

  if (day.morning.length) {
    lines.push('**🌅 Morning**');
    day.morning.forEach(a => lines.push(formatActivity(a)));
    lines.push('');
  }

  if (day.afternoon.length) {
    lines.push('**☀️ Afternoon**');
    day.afternoon.forEach(a => lines.push(formatActivity(a)));
    lines.push('');
  }

  if (day.evening.length) {
    lines.push('**🌙 Evening**');
    day.evening.forEach(a => lines.push(formatActivity(a)));
    lines.push('');
  }

  lines.push(`*Estimated daily spend: ~$${day.estimatedCost}*`, '');
  lines.push('---', '');
  return lines.join('\n');
}

function formatActivity(a: { time: string; name: string; description: string; cost: number; tips?: string }): string {
  const costStr = a.cost === 0 ? 'free' : `~$${a.cost}`;
  const tip = a.tips ? ` _(${a.tips.slice(0, 80)})_` : '';
  return `- **${a.time}** ${a.name} _(${costStr})_${tip}`;
}

/**
 * Format a budget breakdown as a Markdown table.
 */
export function formatBudget(budget: BudgetBreakdown): string {
  const cur = budget.currency;
  const row = (label: string, b: { min: number; max: number }) =>
    `| ${label} | ${formatCurrency(b.min, cur)} | ${formatCurrency(b.max, cur)} |`;

  return [
    '## 💰 Budget Breakdown',
    '',
    '| Category | Min | Max |',
    '|----------|-----|-----|',
    row('Accommodation', budget.accommodation),
    row('Food & Drinks', budget.food),
    row('Activities', budget.activities),
    row('Local Transport', budget.transport),
    row('Miscellaneous', budget.miscellaneous),
    row('**Total**', budget.total),
    '',
    `_Estimates in ${cur}. Flights not included._`,
    '',
  ].join('\n');
}

/**
 * Format a weather forecast as a short Markdown summary.
 */
export function formatWeatherSummary(forecast: WeatherForecast): string {
  const lines = [
    `## 🌤️ Weather Forecast — ${forecast.destination}`,
    `_${forecast.summary}_`,
    '',
    '| Date | High | Low | Conditions | Rain% |',
    '|------|------|-----|------------|-------|',
  ];

  for (const d of forecast.days) {
    lines.push(
      `| ${d.date} | ${d.tempMax}°C | ${d.tempMin}°C | ${d.conditions} | ${d.precipitationChance}% |`,
    );
  }
  lines.push('');
  return lines.join('\n');
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString('en-GB', {
      day: 'numeric', month: 'long', year: 'numeric',
    });
  } catch {
    return iso;
  }
}

function formatCurrency(amount: number, currency: string): string {
  const symbols: Record<string, string> = {
    USD: '$', EUR: '€', GBP: '£', JPY: '¥', AUD: 'A$', CAD: 'C$',
  };
  const sym = symbols[currency] ?? `${currency} `;
  return `${sym}${amount.toLocaleString()}`;
}

function formatWeatherLine(w: WeatherDay): string {
  return `${w.conditions} · ${w.tempMin}–${w.tempMax}°C · Rain ${w.precipitationChance}%`;
}
