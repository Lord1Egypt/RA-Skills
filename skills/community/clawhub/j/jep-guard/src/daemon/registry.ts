import { SkillIdentity } from '../core/types';
import fs from 'fs';
import path from 'path';
import os from 'os';
import nacl from 'tweetnacl';

export class SkillRegistryService {
  private skills = new Map<string, SkillIdentity>();
  private dbPath: string;

  constructor(configDir?: string) {
    const dir = configDir || path.join(os.homedir(), '.jep-guard');
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
    this.dbPath = path.join(dir, 'skill-registry.json');
    this.load();
  }

  register(manifest: Partial<SkillIdentity> & { name: string; version: string }): SkillIdentity {
    const keyPair = nacl.sign.keyPair();

    const skill: SkillIdentity = {
      skill_id: manifest.name,
      name: manifest.name,
      version: manifest.version,
      pubkey: Buffer.from(keyPair.publicKey).toString('base64'),
      capabilities: manifest.capabilities || [],
      risk_level: this.assessRisk(manifest.capabilities || []),
      installed_at: Date.now(),
      last_seen: Date.now(),
      extensions: manifest.extensions || [],
      metadata: {
        author: manifest.metadata?.author,
        source: manifest.metadata?.source || 'clawhub'
      }
    };

    this.skills.set(skill.skill_id, skill);
    this.persist();
    return skill;
  }

  get(skillId: string): SkillIdentity | undefined {
    const s = this.skills.get(skillId);
    if (s) {
      s.last_seen = Date.now();
      this.persist();
    }
    return s;
  }

  list(): SkillIdentity[] {
    return Array.from(this.skills.values());
  }

  verifySignature(skillId: string, message: string, signature: string): boolean {
    const skill = this.skills.get(skillId);
    if (!skill) return false;

    const msgBytes = Buffer.from(message, 'utf-8');
    const sigBytes = Buffer.from(signature, 'base64');
    const pubBytes = Buffer.from(skill.pubkey, 'base64');
    return nacl.sign.detached.verify(msgBytes, sigBytes, pubBytes);
  }

  private assessRisk(caps: string[]): SkillIdentity['risk_level'] {
    if (caps.includes('shell_exec') || caps.includes('system:process_control')) return 'critical';
    if (caps.includes('file_write') || caps.includes('rm')) return 'high';
    if (caps.includes('http_post') || caps.includes('api_call')) return 'medium';
    return 'low';
  }

  private load(): void {
    if (fs.existsSync(this.dbPath)) {
      try {
        const data = JSON.parse(fs.readFileSync(this.dbPath, 'utf-8'));
        for (const s of data.skills || []) this.skills.set(s.skill_id, s);
      } catch (e) {
        console.warn('[JEP Guard] Failed to load skill registry:', e);
      }
    }
  }

  private persist(): void {
    try {
      fs.writeFileSync(this.dbPath, JSON.stringify({ skills: this.list() }, null, 2), { mode: 0o600 });
    } catch (e) {
      console.warn('[JEP Guard] Failed to persist skill registry:', e);
    }
  }
}