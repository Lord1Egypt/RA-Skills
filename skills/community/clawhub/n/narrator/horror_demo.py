#!/usr/bin/env python3
"""
HORROR MODE DEMO - Pure spooky announcer energy
No screenshots needed - just pure horror narration!
"""

import time
import random
import sys

HORROR_PHRASES = [
    "the cursor moves toward the dark abyss of the terminal...",
    "OH NO! A DELETE BUTTON! WILL IT SURVIVE?!",
    "the screen flickers... something ancient awakens...",
    "they're typing a command... whatHaveYouDone.exe",
    "the terminal opens its maw, hungry for input...",
    "darkness fills the command line... a segfault emerges...",
    "the cursor hovers over rm -rf... THE HORROR!",
    "compiling... always compiling... neverending...",
    "a bash script emerges from the shadows...",
    "the ghost of processes past haunts this terminal...",
    "Ctrl+C won't save them now...",
    "sudo... the forbidden word is spoken!",
    "the cursor lingers on /dev/null... it's going in!",
    "AN ERROR MESSAGE! What dark magic is this?!",
    "the power indicator glows red... doom approaches...",
    "they're SSHing into the void... there's no going back!",
    "git push --force... THE NUCLEAR OPTION!",
    "the fan spins up... the processor is SUFFERING!",
    "kernel panic in the distance... running won't help!",
    "THE BLUE SCREEN OF DEATH APPROACHES!",
    "chmod 777... they've doomed us all!",
    "the terminal prompt stares back... judging...",
    "docker-compose up... waking sleeping containers...",
    "npm install... the node_modules beast awakens!",
    "they're editing vim... will they ever ESCAPE?!",
    "the cursor blinks once... then twice... then... it KNOWS!",
    "background processes multiply in the darkness...",
    "the swap file grows... memory bleeds...",
    "ls -la reveals... more than expected...",
    "the autocomplete suggestion... is wrong... SO WRONG!",
]

def horror_narrate():
    """Generate continuous horror commentary."""
    print("🎃" * 20)
    print("🎃" * 20)
    print("\n🎙️ HORROR MODE ACTIVATED 🎙️\n")
    print("   The announcer awakens...\n")
    print("-" * 50)
    
    try:
        idx = 0
        while True:
            phrase = HORROR_PHRASES[idx % len(HORROR_PHRASES)]
            print(f"🎃 \"{phrase}\"")
            sys.stdout.flush()
            
            # Random timing for dramatic effect
            time.sleep(random.uniform(2.5, 4.0))
            
            idx += 1
            
            # Occasional dramatic pause
            if random.random() < 0.15:
                print("\n...silence...\n")
                time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n" + "-" * 50)
        print("\n🎙️ \"AND... scene. Fade to black.\"\n")
        print("🎃" * 20)
        print("🎃" * 20)

if __name__ == '__main__':
    horror_narrate()
