/**
 * explainer.js — Generate plain-English explanations
 */

const PLAIN_EXPLANATIONS = {
  'natural disaster': (d) =>
    `A natural disaster has struck ${d.location}. This poses immediate risk to life and property in the area, with potential knock-on effects on ${d.affectedSystems.join(', ')}. Recovery typically follows patterns seen in similar past events in this region. Historical data helps estimate how long disruption to ${d.affectedSystems.join(', ')} may last.`,

  'corporate': (d) =>
    `A significant corporate event — ${d.title}. In plain terms: this could affect stock prices, jobs, or services tied to the company. If you hold shares, work in the industry, or rely on their products or services, the impact on ${d.affectedSystems.join(', ')} may be directly relevant to your finances or daily life.`,

  'political': (d) =>
    `A political development in ${d.location} is reshaping local or national policy. This could affect ${d.affectedSystems.join(', ')} — from regulations and public services to international trade and travel. Monitor for follow-on effects if this touches your industry or plans.`,

  'conflict': (d) =>
    `A military or security event is unfolding in ${d.location}. Immediate risks include disruptions to ${d.affectedSystems.join(', ')} and potential broader geopolitical fallout. Historical conflicts in similar settings provide estimates of duration and severity.`,

  'economic': (d) =>
    `An economic event is reshaping the landscape in ${d.location}. This could affect ${d.affectedSystems.join(', ')} — including prices, jobs, and financial markets. Long-term impact depends on policy responses, government intervention, and global market reactions.`,

  'health': (d) =>
    `A public health event has emerged in ${d.location}. The primary concern is direct impact on ${d.affectedSystems.join(', ')}. Healthcare systems in similar past outbreaks have followed consistent recovery patterns, which help estimate when normal service resumes.`,

  'climate': (d) =>
    `A climate or environmental event is unfolding in ${d.location}. Effects on ${d.affectedSystems.join(', ')} may be immediate — such as air quality degradation or agricultural disruption — or long-term, such as ecosystem degradation. Historical climate events guide long-term impact projections.`,

  'infrastructure': (d) =>
    `Infrastructure in ${d.location} has been disrupted, affecting ${d.affectedSystems.join(', ')}. Based on comparable past events in this region, repair timelines and service restoration estimates can be derived with reasonable confidence.`,

  'technology': (d) =>
    `A significant technology event has occurred: ${d.title}. This could affect ${d.affectedSystems.join(', ')} — from data privacy and internet access to supply chains for semiconductors and hardware. The long-term impact depends on regulatory responses and market adaptation.`,

  'general news': (d) =>
    `This news from ${d.location} relates to ${d.affectedSystems.join(', ')}. The significance to you depends on your geographic proximity to the area and how these systems feature in your daily life or plans.`,
};

function buildPlainEnglish(data) {
  const fn = PLAIN_EXPLANATIONS[data.eventType] || PLAIN_EXPLANATIONS['general news'];
  return fn(data);
}

module.exports = { buildPlainEnglish };
