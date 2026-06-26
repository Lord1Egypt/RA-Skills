/**
 * gmail-adapter.js
 * Adaptador de Gmail para PhishGuard usando el skill "gog" de OpenClawd.
 *
 * OpenClawd accede a Gmail a traves del CLI "gog" (Google Workspace CLI).
 * Este modulo envuelve esos comandos y los expone con una interfaz limpia
 * que el resto del skill puede usar sin conocer los detalles de gog.
 *
 * Prerequisito: el skill "gog" debe estar instalado y autenticado en OpenClawd.
 * Comandos usados:
 *   gog gmail list    -- lista mensajes
 *   gog gmail read    -- lee un mensaje
 *   gog gmail label   -- agrega etiquetas
 */

import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

// Tiempo limite por comando (ms)
const CMD_TIMEOUT = 15000;

export class GmailAdapter {
  constructor() {
    this.gogAvailable = null; // se verifica en la primera llamada
  }

  /**
   * Verifica que gog este instalado y autenticado.
   * @returns {Promise<{ok: boolean, message: string}>}
   */
  async checkHealth() {
    try {
      await this.run("gog --version");
      this.gogAvailable = true;
      return { ok: true, message: "gog disponible y operativo" };
    } catch {
      this.gogAvailable = false;
      return {
        ok: false,
        message: "El skill 'gog' no esta instalado o no esta autenticado. " +
          "Ejecuta: openclawd skill install gog && gog auth login"
      };
    }
  }

  /**
   * Lista los mensajes no leidos de la bandeja.
   * @param {number} maxResults - cantidad maxima de mensajes (default: 20)
   * @returns {Promise<Array<{id: string, threadId: string}>>}
   */
  async listUnread(maxResults = 20) {
    await this.ensureGog();
    const output = await this.run(
      `gog gmail list --query "is:unread" --max ${maxResults} --format json`
    );
    const parsed = this.parseJson(output, []);
    return Array.isArray(parsed) ? parsed : (parsed.messages ?? []);
  }

  /**
   * Obtiene el contenido completo de un mensaje.
   * @param {string} messageId
   * @returns {Promise<object>} objeto con sender, subject, body, headers, etc.
   */
  async getMessage(messageId) {
    await this.ensureGog();
    const output = await this.run(
      `gog gmail read --id ${messageId} --format json`
    );
    return this.parseJson(output, null);
  }

  /**
   * Agrega una etiqueta a un mensaje (cuarentena o advertencia).
   * @param {string} messageId
   * @param {string} labelName
   */
  async addLabel(messageId, labelName) {
    await this.ensureGog();
    // gog crea la etiqueta automaticamente si no existe
    await this.run(
      `gog gmail label --id ${messageId} --add "${labelName}"`
    );
  }

  /**
   * Parsea el mensaje crudo de gog al formato que usa PhishGuard.
   * @param {object} rawMessage - respuesta JSON de "gog gmail read"
   * @returns {object} emailData compatible con RulesEngine y AIAnalyzer
   */
  parseMessage(rawMessage) {
    if (!rawMessage) return null;

    // gog devuelve los headers ya parseados como objeto
    const headers = rawMessage.headers ?? {};
    const body = rawMessage.body?.plain ?? rawMessage.body?.text ?? rawMessage.snippet ?? "";
    const urls = this.extractUrls(body);

    // Extraer resultados de autenticacion del header Authentication-Results
    const authResults = headers["authentication-results"] ?? "";
    const spfResult = this.extractAuthField(authResults, "spf");
    const dkimResult = this.extractAuthField(authResults, "dkim");

    return {
      messageId: rawMessage.id,
      sender: headers["from"] ?? headers["sender"] ?? "",
      replyTo: headers["reply-to"] ?? null,
      subject: headers["subject"] ?? "(sin asunto)",
      bodyText: body,
      urls,
      spfResult,
      dkimResult,
      attachments: (rawMessage.attachments ?? []).map(a => a.filename ?? a.name ?? ""),
    };
  }

  // ── Helpers privados ───────────────────────────────────────────────────────

  async ensureGog() {
    if (this.gogAvailable === null) {
      const health = await this.checkHealth();
      if (!health.ok) throw new Error(health.message);
    }
    if (!this.gogAvailable) {
      throw new Error("gog no esta disponible. Instala el skill con: openclawd skill install gog");
    }
  }

  async run(command) {
    const { stdout, stderr } = await execAsync(command, { timeout: CMD_TIMEOUT });
    if (stderr && stderr.trim()) {
      // gog puede escribir logs en stderr que no son errores reales
      const isWarning = stderr.toLowerCase().includes("warn") || stderr.toLowerCase().includes("deprecat");
      if (!isWarning) throw new Error(stderr.trim());
    }
    return stdout.trim();
  }

  parseJson(text, fallback) {
    try {
      return JSON.parse(text);
    } catch {
      return fallback;
    }
  }

  extractUrls(text) {
    const urlRegex = /https?:\/\/[^\s"'<>)]+/gi;
    return [...new Set((text ?? "").match(urlRegex) ?? [])];
  }

  extractAuthField(authHeader, field) {
    const match = (authHeader ?? "").match(new RegExp(field + "=([a-z]+)", "i"));
    return match ? match[1].toLowerCase() : null;
  }
}
