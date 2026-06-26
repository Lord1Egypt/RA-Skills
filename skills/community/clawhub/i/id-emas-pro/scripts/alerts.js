// ============================================
// scripts/alerts.js — Alert system
// ============================================

export class AlertManager {
  constructor(storage, notifier) {
    this.storage = storage;
    this.notifier = notifier;
  }

  async createAlert(userId, params) {
    const alert = {
      ...params,
      id: crypto.randomUUID(),
      userId,
      triggered: false,
      createdAt: new Date(),
    };
    await this.storage.saveAlert(alert);
    return alert;
  }

  async deleteAlert(userId, alertId) {
    const alerts = await this.storage.getAlerts(userId);
    const exists = alerts.find((a) => a.id === alertId);
    if (!exists) throw new Error("Alert tidak ditemukan");
    await this.storage.deleteAlert(alertId);
  }

  async listAlerts(userId) {
    return this.storage.getAlerts(userId);
  }

  async checkPrices(userId, currentPrices) {
    const alerts = await this.storage.getAlerts(userId);
    const triggered = [];
    for (const alert of alerts) {
      if (alert.triggered) continue;

      const price = currentPrices.get(alert.brand);
      if (!price) continue;

      const currentValue = alert.type === "buy" ? price.buyPrice : price.sellPrice;

      const shouldTrigger =
        (alert.condition === "above" && currentValue >= alert.targetPrice) ||
        (alert.condition === "below" && currentValue <= alert.targetPrice);

      if (shouldTrigger) {
        await this.storage.markTriggered(alert.id);
        await this.notifier.send(alert, currentValue, price);
        triggered.push({ ...alert, triggered: true });
      }
    }

    return triggered;
  }
}

export class ChatNotifier {
  constructor(sendMessage) {
    this.sendMessage = sendMessage;
  }

  async send(alert, currentPrice, priceData) {
    const direction = alert.condition === "above" ? "naik ke atas" : "turun di bawah";
    const type = alert.type === "buy" ? "beli" : "jual";
    const fmt = (n) => `Rp ${n.toLocaleString("id-ID")}`;
    const message = [
      `🔔 *Alert Emas Triggered!*`,
      ``,
      `Brand: ${priceData.brand}`,
      `Kondisi: Harga ${type} ${direction} ${fmt(alert.targetPrice)}`,
      `Harga sekarang: ${fmt(currentPrice)}/gram`,
      `Waktu: ${new Date().toLocaleString("id-ID")}`,
    ].join("\n");

    await this.sendMessage(alert.userId, message);
  }
}

export function formatAlertList(alerts) {
  if (alerts.length === 0) return "Kamu belum punya alert aktif.";

  return alerts
    .map((a, i) => {
      const status = a.triggered ? "✅ triggered" : "⏳ aktif";
      return `${i + 1}. ${a.brand} — harga ${a.type} ${a.condition} Rp ${a.targetPrice.toLocaleString("id-ID")} [${status}] (id: ${a.id.slice(0, 8)})`;
    })
    .join("\n");
}
