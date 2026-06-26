#!/usr/bin/env python3
import os
import subprocess
import time
import sys

sys.path.insert(0, os.path.dirname(__file__))
from speaker_verification import enroll_speaker

MIC_DEVICE = os.environ.get("ALFRED_MIC", "hw:Array,0")
SPEAKER_DEVICE = os.environ.get("ALFRED_SPEAKER", "hw:C2c,0")

def play_beep():
    # Simple beep tone using aplay on our active speaker
    try:
        plug = 'plughw:' + SPEAKER_DEVICE.replace('hw:', '')
        subprocess.run(['aplay', '-q', '-D', plug, '-d', '1', '/usr/share/sounds/alsa/Front_Center.wav'], capture_output=True)
    except:
        pass

def main():
    print("=== Jarvis Voice Biometric Enrollment ===")
    print("We will record 4 voice samples of you speaking (about 3 seconds each).")
    print("Please speak a natural command when instructed, such as:")
    print("  'Hey Jarvis, turn off the living room lights.'")
    print("  'Hey Jarvis, open the 3D printer.'")
    print("--------------------------------------------------")
    
    enrollment_files = []
    
    for i in range(1, 5):
        print(f"\n[Sample {i}/4] Get ready...")
        time.sleep(1.5)
        print("🎙️ SPEAK NOW!")
        play_beep()
        
        out_wav = f"/tmp/enroll_manos_{i}.wav"
        # Record 3.5 seconds
        cmd = [
            'arecord',
            '-D', MIC_DEVICE,
            '-f', 'S24_3LE',
            '-r', '16000',
            '-c', '2',
            '-d', '4',
            '-q',
            out_wav
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("✅ Recorded. Processing...")
            enrollment_files.append(out_wav)
        except Exception as e:
            print(f"❌ Recording failed: {e}")
            return
            
    print("\n📦 Training GMM model on your voice...")
    try:
        threshold = enroll_speaker(enrollment_files)
        print("\n🎉 SUCCESS!")
        print("Your voice profile GMM model is now saved and calibrated!")
        print("You can now enable voice verification in your pipeline.")
    except Exception as e:
        print(f"❌ Enrollment failed: {e}")

if __name__ == "__main__":
    main()
