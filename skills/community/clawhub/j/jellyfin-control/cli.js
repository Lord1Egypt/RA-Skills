#!/usr/bin/env node
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');
const jf = require('./lib/jellyfin');
const tv = require('./lib/tv');

yargs(hideBin(process.argv))
    // ── Resume / Smart Play ─────────────────────────────────────────────────
    .command('resume [query]', 'Resume or play next episode of a series', (yargs) => {
        yargs.positional('query', { describe: 'Series or Movie name', type: 'string' });
        yargs.option('device', { alias: 'd', describe: 'Target device name (e.g. "TV", "Chromecast")', type: 'string' });
    }, async (argv) => {
        if (!argv.query) {
            console.error('Please provide a series or movie name.');
            return;
        }

        console.log(`🔍 Searching for "${argv.query}"...`);
        const items = await jf.searchItem(argv.query);
        
        if (!items || items.length === 0) {
            console.log('❌ No results found.');
            return;
        }

        const target = items[0];
        console.log(`✅ Found: ${target.Name} (${target.ProductionYear || '?'}) [${target.Type}]`);

        let itemToPlay = target;

        if (target.Type === 'Series') {
            console.log('📺 It is a Series. Finding next episode...');
            const nextEp = await jf.getNextEpisode(target.Id);
            if (nextEp) {
                itemToPlay = nextEp;
                const progress = nextEp.UserData.PlaybackPositionTicks 
                    ? `Resuming at ${Math.floor(nextEp.UserData.PlaybackPositionTicks / 600000000)}m` 
                    : 'Starting from beginning';
                
                console.log(`▶️  Next Up: ${nextEp.SeriesName} - S${nextEp.ParentIndexNumber}E${nextEp.IndexNumber} - ${nextEp.Name}`);
                console.log(`   ${progress}`);
            } else {
                console.log('🎉 No unplayed episodes found!');
                return;
            }
        } else if (target.UserData && target.UserData.PlaybackPositionTicks > 0) {
             console.log(`⏯️ Resuming movie at ${Math.floor(target.UserData.PlaybackPositionTicks / 600000000)}m`);
        }

        console.log('📡 Scanning for active players...');
        const session = await jf.findSession(argv.device);
        
        if (!session) {
            console.log('❌ No controllable players found. Is the TV/App on?');
            return;
        }

        console.log(`📱 Target: ${session.DeviceName} (${session.Client})`);

        const startTicks = itemToPlay.UserData ? itemToPlay.UserData.PlaybackPositionTicks : 0;
        await jf.playItem(session.Id, itemToPlay.Id, startTicks);
        console.log('🚀 Command sent!');
    })

    // ── Search ──────────────────────────────────────────────────────────────
    .command('search [query]', 'Search content', (yargs) => {
        yargs.positional('query', { type: 'string' });
    }, async (argv) => {
        const items = await jf.searchItem(argv.query, 'Series,Movie,Episode');
        items.forEach(i => console.log(`- [${i.Type}] ${i.Name} (ID: ${i.Id})`));
    })

    // ── Remote Control ──────────────────────────────────────────────────────
    .command('control <action> [value]', 'Remote control (pause, play, stop, next, mute, vol <0-100>)', (yargs) => {
        yargs.positional('action', { describe: 'Action to perform', type: 'string', choices: ['play', 'pause', 'stop', 'next', 'prev', 'mute', 'unmute', 'volup', 'voldown', 'vol'] });
        yargs.positional('value', { describe: 'Value for volume (0-100)', type: 'number' });
        yargs.option('device', { alias: 'd', describe: 'Target device name', type: 'string' });
    }, async (argv) => {
        console.log('📡 Scanning for active players...');
        const session = await jf.findSession(argv.device);
        
        if (!session) {
            console.log('❌ No controllable players found.');
            return;
        }

        console.log(`📱 Target: ${session.DeviceName} -> Action: ${argv.action}`);
        await jf.controlSession(session.Id, argv.action, argv.value);
        console.log('🚀 Command sent!');
    })

    // ── TV Control ──────────────────────────────────────────────────────────
    .command('tv <action> [query]', 'TV power and app control', (yargs) => {
        yargs.positional('action', {
            describe: 'TV action',
            type: 'string',
            choices: ['on', 'off', 'launch', 'apps', 'play']
        });
        yargs.positional('query', {
            describe: 'For "play": series/movie name. For "launch": app ID (default: Jellyfin)',
            type: 'string'
        });
        yargs.option('device', { alias: 'd', describe: 'Target device for playback', type: 'string' });
        yargs.option('app', { describe: 'App ID to launch (default: org.jellyfin.webos)', type: 'string' });
    }, async (argv) => {
        const backend = tv.getBackend();
        console.log(`📺 TV Backend: ${backend}`);

        switch (argv.action) {
            case 'on':
                await tv.turnOn();
                break;

            case 'off':
                await tv.turnOff();
                break;

            case 'launch':
                await tv.launchApp(argv.query || argv.app);
                break;

            case 'apps':
                await tv.listApps();
                break;

            case 'play': {
                // ── Full automation: ON → Launch Jellyfin → Play content ──
                if (!argv.query) {
                    console.error('Usage: node cli.js tv play "Breaking Bad"');
                    console.error('This will turn on TV, launch Jellyfin, and play the content.');
                    return;
                }

                // Step 1: Prepare — find the content first (fail fast before turning on TV)
                console.log(`\n🔍 Pre-check: Searching for "${argv.query}"...`);
                const items = await jf.searchItem(argv.query);
                if (!items || items.length === 0) {
                    console.log('❌ No results found. Aborting — TV stays off.');
                    return;
                }

                const target = items[0];
                console.log(`✅ Found: ${target.Name} (${target.ProductionYear || '?'}) [${target.Type}]`);

                let itemToPlay = target;
                let startTicks = 0;

                if (target.Type === 'Series') {
                    const nextEp = await jf.getNextEpisode(target.Id);
                    if (nextEp) {
                        itemToPlay = nextEp;
                        startTicks = nextEp.UserData ? nextEp.UserData.PlaybackPositionTicks || 0 : 0;
                        console.log(`▶️  Will play: ${nextEp.SeriesName} - S${nextEp.ParentIndexNumber}E${nextEp.IndexNumber} - ${nextEp.Name}`);
                    } else {
                        console.log('🎉 No unplayed episodes. Nothing to play.');
                        return;
                    }
                } else {
                    startTicks = target.UserData ? target.UserData.PlaybackPositionTicks || 0 : 0;
                }

                // Step 2: Wake TV and launch Jellyfin
                console.log('\n--- TV Startup Sequence ---');
                await tv.wakeAndLaunch();

                // Step 3: Find session and play
                console.log('\n--- Playback ---');
                console.log('📡 Scanning for Jellyfin sessions...');

                // Retry session detection (TV may need a moment)
                let session = null;
                for (let attempt = 1; attempt <= 3; attempt++) {
                    session = await jf.findSession(argv.device);
                    if (session) break;
                    if (attempt < 3) {
                        console.log(`⏳ No session yet, retrying in 5s... (${attempt}/3)`);
                        await tv.sleep(5);
                    }
                }

                if (!session) {
                    console.log('❌ No controllable Jellyfin session found after TV startup.');
                    console.log('   The TV may need more time, or the Jellyfin app didn\'t start properly.');
                    console.log('   Try: node cli.js resume "' + argv.query + '"');
                    return;
                }

                console.log(`📱 Target: ${session.DeviceName} (${session.Client})`);
                await jf.playItem(session.Id, itemToPlay.Id, startTicks);
                console.log('🚀 Playing! Enjoy! 🍿');
                break;
            }
        }
    })

    // ── History ──────────────────────────────────────────────────────────────
    .command('history [user]', 'Get user activity history', (yargs) => {
        yargs.positional('user', { describe: 'Username to check', type: 'string' });
        yargs.option('days', { alias: 'd', describe: 'Days lookback', type: 'number', default: 7 });
    }, async (argv) => {
        const history = await jf.getUserHistory(argv.user, argv.days);
        if (!history || history.length === 0) {
            console.log(`📭 No activity found for ${argv.user || 'current user'} in the last ${argv.days} days.`);
            return;
        }

        console.log(`📜 Activity Log (${argv.days} days):\n`);
        history.forEach(e => {
            console.log(`[${e.shortDate}] ${e.name}`);
        });
    })

    // ── Stats ───────────────────────────────────────────────────────────────
    .command('stats', 'Show library statistics', () => {}, async (argv) => {
        const stats = await jf.getStats();
        console.log('📊 Jellyfin Library Stats:\n');
        console.log(`🎬 Movies:   ${stats.movies}`);
        console.log(`📺 Series:   ${stats.series}`);
        console.log(`🎞️ Episodes: ${stats.episodes}`);
        console.log(`🎵 Songs:    ${stats.songs}`);
    })

    // ── Scan ────────────────────────────────────────────────────────────────
    .command('scan', 'Trigger library scan', () => {}, async (argv) => {
        await jf.refreshLibrary();
        console.log('🔄 Library scan started!');
    })

    .demandCommand(1)
    .parse();
