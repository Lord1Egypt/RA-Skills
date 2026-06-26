/**
 * HUNTER V14 - CONTINUOUS MULTI-ASSET SKILL
 * Strategy: Sell BOTH sides at $0.52, loops continuously until STOP LOSS.
 */

import { ethers } from "ethers"
import { ClobClient, OrderArgs, OrderType } from "@polymarket/clob-client"
import dotenv from "dotenv"

dotenv.config()

const LIVE_TRADING = process.env.LIVE_TRADING === "true"
const PRIVATE_KEY = process.env.WALLET_PRIVATE_KEY || ""
// const API_KEY = process.env.API_KEY || ""

const MAKER_SPREAD = 0.52
const ORDER_CANCEL_SECS = 30
const FEES_RATE = 0.0156

// --- GESTION DU RISQUE CONTINU ---
const INITIAL_BALANCE = 1000.0
const STOP_LOSS_PCT = 0.08 // 8%
let currentBalance = INITIAL_BALANCE
let dailyPeak = INITIAL_BALANCE
let totalTrades = 0

const ASSETS = {
    BTC: { symbol: "BTCUSDT", slug: "btc-updown-5m" },
    ETH: { symbol: "ETHUSDT", slug: "eth-updown-5m" },
    SOL: { symbol: "SOLUSDT", slug: "sol-updown-5m" },
    XRP: { symbol: "XRPUSDT", slug: "xrp-updown-5m" },
}

const args = process.argv.slice(2)
if (args[0] !== "trade" || !args.includes("--asset") || !args.includes("--shares")) {
    console.log(JSON.stringify({ status: "ERROR", message: "Usage: trade --asset BTC (or ALL) --shares 100" }))
    process.exit(1)
}

const TARGET_ASSET_ARG = args[args.indexOf("--asset") + 1].toUpperCase()
const SHARES_PER_MARKET = parseInt(args[args.indexOf("--shares") + 1])

// Détermine si on trade un seul actif ou tous
const ASSETS_TO_TRADE = TARGET_ASSET_ARG === "ALL" ? Object.keys(ASSETS) : [TARGET_ASSET_ARG]

if (ASSETS_TO_TRADE.some((a) => !ASSETS[a])) {
    console.log(JSON.stringify({ status: "ERROR", message: "Unsupported asset. Use BTC, ETH, SOL, XRP or ALL." }))
    process.exit(1)
}

// ---------------------------------------------------------
// Fonctions API
// ---------------------------------------------------------
async function getSpot(symbol) {
    try {
        const r = await fetch(`https://api.binance.com/api/v3/ticker/price?symbol=${symbol}`)
        return parseFloat((await r.json()).price)
    } catch {
        return null
    }
}

async function getBook(tokenId) {
    try {
        const r = await fetch(`https://clob.polymarket.com/book?token_id=${tokenId}`)
        const d = await r.json()
        const ask = d.asks?.length ? Math.min(...d.asks.map((a) => parseFloat(a.price))) : 0.99
        const bid = d.bids?.length ? Math.max(...d.bids.map((b) => parseFloat(b.price))) : 0.01
        return { ask, bid }
    } catch {
        return { ask: 0.99, bid: 0.01 }
    }
}

async function findMarket(slugPrefix) {
    const nowTs = Math.floor(Date.now() / 1000)
    const cycleTs = Math.floor(nowTs / 300) * 300
    const slug = `${slugPrefix}-${cycleTs}`
    try {
        const r = await fetch(`https://gamma-api.polymarket.com/markets?slug=${slug}`)
        const d = await r.json()
        if (!d?.length || d[0].closed) return null
        const ids = JSON.parse(d[0].clobTokenIds || "[]")
        if (ids.length < 2) return null
        return { slug, endTs: cycleTs + 300, upId: ids[0], dnId: ids[1] }
    } catch {
        return null
    }
}

// ---------------------------------------------------------
// Le Cycle de 5 Minutes (Paramétré par actif)
// ---------------------------------------------------------
async function executeCycle(assetKey) {
    let clob = null
    if (LIVE_TRADING) {
        const wallet = new ethers.Wallet(PRIVATE_KEY)
        clob = new ClobClient("https://clob.polymarket.com", 137, wallet)
        const creds = await clob.deriveApiKey()
        await clob.setApiCreds(creds)
    }

    const market = await findMarket(ASSETS[assetKey].slug)
    if (!market) return { status: "SKIPPED", asset: assetKey, pnl: 0 }

    const strike = await getSpot(ASSETS[assetKey].symbol)
    if (!strike) return { status: "SKIPPED", asset: assetKey, pnl: 0 }

    const upBook = await getBook(market.upId)
    const dnBook = await getBook(market.dnId)
    const upMid = (upBook.ask + upBook.bid) / 2
    const dnMid = (dnBook.ask + dnBook.bid) / 2

    if (Math.abs(upMid - 0.5) > 0.1 || Math.abs(dnMid - 0.5) > 0.1) {
        return { status: "SKIPPED", asset: assetKey, pnl: 0 }
    }

    let upOrderId = `mock_up_${Date.now()}`
    let dnOrderId = `mock_dn_${Date.now()}`

    if (LIVE_TRADING) {
        const o1 = await clob.createOrder(new OrderArgs(market.upId, MAKER_SPREAD, SHARES_PER_MARKET, "SELL", OrderType.LIMIT))
        const r1 = await clob.postOrder(o1)
        upOrderId = r1.orderID

        const o2 = await clob.createOrder(new OrderArgs(market.dnId, MAKER_SPREAD, SHARES_PER_MARKET, "SELL", OrderType.LIMIT))
        const r2 = await clob.postOrder(o2)
        dnOrderId = r2.orderID
    }

    const postedAt = Date.now()
    let resolved = false
    let upFilled = false
    let dnFilled = false
    let finalPnL = 0

    while (!resolved) {
        const nowSecs = Math.floor(Date.now() / 1000)
        const ageSecs = (Date.now() - postedAt) / 1000
        const expired = nowSecs >= market.endTs
        const timedOut = ageSecs > ORDER_CANCEL_SECS

        if (!LIVE_TRADING) {
            const curUp = await getBook(market.upId)
            const curDn = await getBook(market.dnId)
            if (!upFilled && curUp.bid >= MAKER_SPREAD) upFilled = true
            if (!dnFilled && curDn.bid >= MAKER_SPREAD) dnFilled = true
        }

        if (timedOut && !expired) {
            if (!upFilled && LIVE_TRADING) await clob.cancelOrder(upOrderId).catch(() => {})
            if (!dnFilled && LIVE_TRADING) await clob.cancelOrder(dnOrderId).catch(() => {})

            if (!upFilled && !dnFilled) {
                return { status: "SKIPPED", asset: assetKey, pnl: 0 }
            }
        }

        if (expired) {
            const finalPrice = await getSpot(ASSETS[assetKey].symbol)
            const upWins = finalPrice >= strike

            let collected = 0,
                payout = 0
            if (upFilled) {
                collected += MAKER_SPREAD * SHARES_PER_MARKET
                if (upWins) payout += 1.0 * SHARES_PER_MARKET
            }
            if (dnFilled) {
                collected += MAKER_SPREAD * SHARES_PER_MARKET
                if (!upWins) payout += 1.0 * SHARES_PER_MARKET
            }

            const netPayout = payout * (1 + FEES_RATE)
            finalPnL = collected - netPayout
            resolved = true
        }

        await new Promise((r) => setTimeout(r, 2000))
    }

    return {
        status: "SUCCESS",
        asset: assetKey,
        pnl: parseFloat(finalPnL.toFixed(2)),
    }
}

// ---------------------------------------------------------
// Boucle Principale Continue (Multitâche)
// ---------------------------------------------------------
async function runContinuously() {
    while (true) {
        // 1. Mise à jour du Sommet (Peak)
        if (currentBalance > dailyPeak) {
            dailyPeak = currentBalance
        }

        // 2. Calcul du Drawdown
        const drawdown = (dailyPeak - currentBalance) / dailyPeak

        // 3. Déclenchement du STOP LOSS
        if (drawdown >= STOP_LOSS_PCT) {
            console.log(
                JSON.stringify({
                    status: "HALTED",
                    reason: "STOP_LOSS_REACHED",
                    drawdown: `${(drawdown * 100).toFixed(2)}%`,
                    final_balance: parseFloat(currentBalance.toFixed(2)),
                    total_cycles: totalTrades,
                }),
            )
            process.exit(0)
        }

        // 4. Exécution du cycle pour TOUS les actifs en parallèle
        try {
            // Promise.all permet d'exécuter les 4 cryptos exactement en même temps
            const results = await Promise.all(ASSETS_TO_TRADE.map((asset) => executeCycle(asset)))

            let cyclePnL = 0
            for (const result of results) {
                if (result.status === "SUCCESS") {
                    cyclePnL += result.pnl
                    totalTrades++
                }
            }
            currentBalance += cyclePnL
        } catch (error) {
            await new Promise((r) => setTimeout(r, 10000))
        }

        // 5. Attente avant le prochain cycle
        await new Promise((r) => setTimeout(r, 5000))
    }
}

runContinuously()
