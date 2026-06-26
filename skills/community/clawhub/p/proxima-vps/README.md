# Proxima VPS Setup Skill

Skill ini dipakai untuk membantu AI agent seperti OpenClaw, Hermes Agent, atau agent lain yang mendukung AgentSkills agar bisa men-setup **Proxima di VPS Ubuntu** dengan GUI remote dan MCP access yang aman.

## Tujuan

Skill ini membimbing agent untuk:

- install dan menjalankan Proxima di VPS
- menjalankan Electron sebagai **user non-root**
- menyiapkan GUI virtual dengan **XFCE + Xvfb**
- membuka akses remote lewat:
  - **VNC** di `127.0.0.1:5902`
  - **noVNC** di `127.0.0.1:6081`
- mengaktifkan **REST API** di `127.0.0.1:3210`
- menyediakan **MCP via SSH stdio** lewat command:

```bash
ssh -T proxima-vps proxima-mcp
```

- menyiapkan config untuk IDE lokal seperti:
  - Antigravity
  - Windsurf
  - Zed

## Kapan dipakai

Gunakan skill ini ketika user meminta salah satu dari hal berikut:

- install Proxima di VPS
- setup GUI remote untuk Proxima
- mengatasi error Electron root / sandbox
- membuat REST Proxima bisa diakses dari laptop lewat SSH tunnel
- membuat MCP Proxima bisa dipakai dari IDE lokal
- troubleshooting koneksi MCP, noVNC, VNC, atau REST

## Struktur skill

```text
proxima-vps-setup/
├── SKILL.md
├── README.md
└── references/
    ├── security-and-architecture.md
    ├── server-setup-runbook.md
    ├── local-access-and-mcp.md
    └── troubleshooting.md
```

## Isi file

### `SKILL.md`
Entry point utama skill. Menjelaskan trigger, aturan inti, workflow, dan file referensi yang harus dibaca agent.

### `references/security-and-architecture.md`
Menjelaskan:
- arsitektur deployment
- batas exposure yang aman
- caveat keamanan Proxima
- caveat model routing / `/v1/models`

### `references/server-setup-runbook.md`
Runbook server-side lengkap:
- package Ubuntu yang harus diinstall
- pembuatan user `proxima`
- setup Node global untuk non-root
- service systemd GUI
- service `proxima-app`
- wrapper `proxima-mcp`
- validasi akhir

### `references/local-access-and-mcp.md`
Menjelaskan:
- SSH tunnel untuk GUI/REST
- config `~/.ssh/config`
- config MCP untuk Antigravity, Windsurf, Zed
- cara test MCP dari IDE

### `references/troubleshooting.md`
Berisi kasus umum seperti:
- `curl localhost:3210` gagal dari laptop
- Electron error root sandbox
- MCP IDE gagal connect
- `ERR_INVALID_HTTP_RESPONSE` di port 5902
- noVNC clipboard jelek

## Prinsip arsitektur

Skill ini mengikuti prinsip berikut:

1. **Jangan jalankan Electron sebagai root**
2. **Jangan expose port sensitif ke internet publik**
3. **Bind semua service ke loopback bila memungkinkan**
4. **Gunakan SSH tunnel untuk GUI dan REST**
5. **Gunakan SSH stdio untuk MCP**, bukan public TCP port
6. **Verifikasi hasil nyata**, bukan asumsi

## End state yang diharapkan

Setup dianggap selesai jika:

- `proxima-app.service` aktif
- `127.0.0.1:3210` aktif untuk REST
- `127.0.0.1:5902` aktif untuk VNC
- `127.0.0.1:6081` aktif untuk noVNC
- `ssh -T proxima-vps proxima-mcp` berhasil
- IDE lokal bisa mendeteksi MCP server `proxima-vps`

## Catatan keamanan

Skill ini tidak menyatakan Proxima sebagai aplikasi yang sepenuhnya aman.

Posisi yang benar:
- relatif aman untuk download source
- tidak ideal untuk mesin utama / laptop utama
- lebih cocok dijalankan di VPS atau VM terisolasi
- tetap ada risiko operasional karena browser automation, session cookies, file access, dan temuan bypass TLS di audit sebelumnya

## Packaging

Skill package hasil build tersedia sebagai:

```text
/root/.openclaw/workspace/dist/proxima-vps-setup.skill
```

## Ringkas

Kalau agent lain diberi skill ini, seharusnya agent bisa mengerjakan setup Proxima VPS dari awal sampai siap dipakai melalui GUI, REST, dan MCP tanpa perlu dipandu ulang lewat banyak prompt kecil.
