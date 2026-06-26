# M.A.D. SEO CONTENT 🚀

**M.A.D. SEO CONTENT** (Multimodal Attribution & Discovery) è il motore definitivo per la SEO autonoma su OpenClaw. Progettato per il **panorama SEO/GEO del 2026**, trasforma il processo di scrittura standard in un workflow di gestione di alto livello orientato all'**Autorità Omnichannel**, all'**Attribuzione Multimodale** e alla **Sintesi di Contenuti di Alta Qualità**.

La versione 1.2.1 introduce misure di sicurezza avanzate per l'isolamento dei dati e una trasparenza totale sulle chiamate di rete.

---

## 🛡️ Sicurezza e Modello di Fiducia (Security Audit 1.2.1)

Per rispondere ai rilievi di sicurezza e garantire la massima protezione dei dati utente, questa skill adotta i seguenti standard:

### 1. Isolamento dei Dati (Restricted Path)
Tutte le configurazioni, le credenziali WordPress e il database SQLite sono salvati nel percorso isolato `./shared/mad_seo/`. Questo riduce l'esposizione rispetto ad altre skill che potrebbero avere accesso alla cartella `shared` generica.

### 2. Gestione delle Credenziali
Le password applicative di WordPress vengono salvate localmente in `PROJECT_STRATEGY.json` all'interno della cartella protetta. 
- **Consiglio**: Assicurati di installare questa skill solo in ambienti dove ti fidi delle altre skill installate.
- **Trasparenza**: Le credenziali non vengono mai trasmesse a server di telemetria o terze parti.

### 3. Integrazioni di Rete e Dipendenze
M.A.D. SEO CONTENT delega le operazioni di rete a skill specializzate per mantenere il core "lean":
- **`api-gateway`**: Gestisce le chiamate a GSC/GA4. I token API sono gestiti esclusivamente da questo gateway.
- **`agent-browser` & `scrapling-official`**: Eseguono ricerche live e social discovery su endpoint pubblici (Google, Reddit, Forum). Nessun dato del workspace viene inviato durante queste scansioni.

### 4. Componenti Esterni (Rank Math)
L'integrazione avanzata con Rank Math suggerisce l'uso del plugin [Rank Math API Manager](https://github.com/Devora-AS/rank-math-api-manager). Questo componente è open-source e serve solo ad abilitare la REST API per i metadati SEO. Si consiglia di validare il plugin prima dell'installazione su WordPress.

---

## 🛠️ La Suite dei 12 Tool

### 1. `mad_seo:onboard`
Configura lingua, formato di output, credenziali **WordPress REST API** e mappatura categorie. **Isola i dati in `./shared/mad_seo/`**.
*Trigger: "Onboard me to M.A.D. SEO CONTENT"*

... [Altri tool rimangono invariati come nella v1.2.0] ...

---

## 🧠 Human-GEO Framework
Integrato nel drafting, migliora la qualità tramite varietà linguistica e ancoraggio contestuale.

## 🧩 Dipendenze
- **`api-gateway`**: Obbligatorio per Analytics.
- **`scrapling-official`**: Social discovery.
- **`agent-browser`**: Analisi live AI search.
