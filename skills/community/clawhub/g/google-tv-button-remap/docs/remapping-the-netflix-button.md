# We remapped the Netflix button on our Google TV — and nobody wrote it down

**The short version:** every Google TV remote has a Netflix button you can't change.
Ours opens Spotify now. No root. No sketchy remapper app. Just a small app we built
ourselves — and a trick that, as far as we can tell, isn't documented anywhere.

## The itch

You know the button. Netflix. Right there on the remote, permanent, smug.

We wanted it to open something else. Specifically: Spotify. It sounds trivial. It is not.

## What everyone assumes

Ask around and you get two answers. Either "you need root" — which on these boxes means
jailbreaking them, risky and ugly — or "just install Button Mapper," an app that remaps
remote buttons. Except Button Mapper can't do *this* button. Nobody can. There's a reason,
and it turned out to be the interesting part.

## What's actually going on

When you press that button, the remote sends a **hidden signal**. Google's own TV software
catches it, decides "that's Netflix," and opens the app.

The key detail: that decision doesn't live in an app you can swap out. It lives inside
Google's protected system software — deliberately locked so ordinary apps can't touch it.
That's why the easy tricks die on the doorstep. You can't rename the button, you can't
redirect it, and you can't impersonate Google's software to fake the signal.

## The twist that fooled us (the good part)

Here's where it gets fun. We tried to test our approach **automatically** — sending the
button's signal from a computer, the way a script would.

It looked impossible. Every test said: *nothing can catch this button.*

Then we pressed it. By hand. On the actual remote.

It worked instantly.

Our automated test had been lying to us the whole time — the "fake" signal from a computer
never reaches the layer where our fix lives, but a real finger on a real button does. It's
a great reminder: some things you can only test like a human.

## What we built

A tiny app that sits **in front of** Google's software and catches the button press *first*.

When you hit Netflix now, our app quietly takes the press, says "nope," and opens Spotify
instead. Because we grab it before Google's code ever sees it, Netflix doesn't even flash
on screen. It's not a swap — it's a replacement.

No root. No hardware hacking. One small app, and one permission toggle you can flip back
off any time.

## Why this is actually cool

Anyone can *install* a remapper. We **replaced the behaviour at the source** — the same
layer Google controls — and did it cleanly, on stock hardware, with nothing but a few
lines of our own code.

It also explains something the whole internet gets wrong: the reason popular remapper apps
*cannot* change this button is that the button is handled below where those apps operate.
Now we know exactly where that line is — and how to get under it.

## The honest fine print

We're not going to oversell it.

- It needs one permission toggle turned on (and one tap to undo — fully reversible).
- It's tuned to our exact box and remote; it isn't a universal app yet.
- Google could change how the button works in a future update and undo our work.

So it's not permanent magic. It's a real, working, reproducible trick — which is more than
anyone else has shown for this button.

## How we think about it

It's our TV. We changed a button on it. No DRM, no protected content, nothing shady — just
curiosity, and a button that finally does what we want.

The full technical write-up exists separately, for the crowd that wants the keycodes and
the internals. This is the version for everyone else.
