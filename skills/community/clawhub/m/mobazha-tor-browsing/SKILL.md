---
name: tor-browsing
description: Configure Tor Browser to access Mobazha stores privately, or run a store as a .onion hidden service. Use for privacy and anonymity setup.
---

# Tor Browsing & Privacy Configuration

Access Mobazha stores anonymously through Tor, or run your own store as a .onion hidden service.

## Part A: Browse Mobazha Stores via Tor (Buyer)

### Step 1: Install Tor Browser

Download from the official Tor Project website: <https://www.torproject.org/download/>

| Platform | Install Method |
|----------|---------------|
| Windows | Download and run the installer from torproject.org |
| macOS | Download the `.dmg`, drag to Applications |
| Linux | `sudo apt install torbrowser-launcher` or download from torproject.org |
| Android | Install "Tor Browser" from Google Play or F-Droid |

### Step 2: Access a .onion Store

If a Mobazha store has Tor enabled, it will have a `.onion` address. Open Tor Browser and navigate to:

```
http://<store-onion-address>.onion
```

The store looks and works exactly like the clearnet version, but your connection is routed through the Tor network for privacy.

### Step 3: Browse the Mobazha Marketplace via Tor

The SaaS marketplace can also be accessed through Tor by visiting:

```
https://app.mobazha.org
```

Tor Browser handles the connection routing automatically. Note that `.onion` addresses provide stronger anonymity than accessing clearnet URLs through Tor.

### Privacy Tips for Buyers

- **Use Tor Browser exclusively** — don't use a regular browser with a Tor proxy
- **Don't maximize the window** — keeping the default size reduces fingerprinting
- **Avoid logging in** — browsing without an account provides the strongest anonymity
- **Use cryptocurrency** — for truly private purchases, pay with privacy-focused coins like Zcash (shielded)

## Part B: Run Your Store as a Tor Hidden Service (Seller)

### Option 1: Enable During Docker Installation

```bash
curl -sSL https://get.mobazha.org/standalone | sudo bash -s -- --overlay tor
```

This sets up your store with a `.onion` address. No domain name or public IP required.

### Option 2: Enable on an Existing Docker Store

In the store admin dashboard:

1. Go to **Admin → System → Network**
2. Enable the Tor overlay
3. Save and wait for the service to restart

The `.onion` address will be generated and displayed in the Network settings.

No re-installation needed.

### Option 3: Using mobazha-ctl

```bash
cd /opt/mobazha
# Update .env to set OVERLAY_TYPE=tor and CONNECTIVITY=overlay
# Then restart:
docker compose -f docker-compose.yml -f docker-compose.overlay.yml --profile tor up -d
```

### Finding Your .onion Address

After enabling Tor, your store's `.onion` address is shown in:

- **Admin → System → Network** in the dashboard
- The container logs: `docker compose logs | grep "onion"`

### How It Works

When Tor overlay is enabled:

- Your store runs a Tor hidden service inside the Docker container
- A `.onion` address is generated (no domain purchase needed)
- Buyers can access your store anonymously via Tor Browser
- Your VPS IP is not exposed to buyers
- You can run with Tor **and** a clearnet domain simultaneously

### Lokinet Alternative

Mobazha also supports Lokinet as a privacy overlay:

```bash
curl -sSL https://get.mobazha.org/standalone | sudo bash -s -- --overlay lokinet
```

Lokinet provides similar anonymity properties with potentially lower latency.

## Security Considerations

- **Tor does not encrypt stored data** — it protects network traffic only
- If running a hidden service, keep your VPS identity separate from your real identity
- Use cryptocurrency for payments to maintain transaction privacy
- Regularly update your store to get the latest security patches
