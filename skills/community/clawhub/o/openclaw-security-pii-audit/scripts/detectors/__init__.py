"""PII detector registry."""

from .phone import PhoneDetector
from .email_detector import EmailDetector
from .national_id import NationalIdDetector
from .passport import PassportDetector
from .bank_card import BankCardDetector
from .person_name import PersonNameDetector
from .address import AddressDetector
from .social_account import SocialAccountDetector

ALL_DETECTORS = [
    PhoneDetector(),
    EmailDetector(),
    NationalIdDetector(),
    PassportDetector(),
    BankCardDetector(),
    PersonNameDetector(),
    AddressDetector(),
    SocialAccountDetector(),
]
